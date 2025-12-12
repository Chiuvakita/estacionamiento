from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from .models import Usuario
from .forms.usuarios import UsuarioForm, RegistroClienteForm
from apps.utils.decoradores import loginRequerido, sinLogin, soloAdminEmpleado
import requests
import json
from django.conf import settings
from django.contrib.auth.models import User

@loginRequerido
def homeCliente(request):
    if hasattr(request.user, 'username') and request.user.username.isdigit():
        rut = int(request.user.username)
        try:
            usuario = Usuario.objects.get(rut=rut)
            if usuario.rol == 'Cliente':
                return render(request, 'homeCliente.html')
        except Usuario.DoesNotExist:
            pass
    return redirect('login')


@loginRequerido
@soloAdminEmpleado
def homeAdmin(request):
    return render(request, 'homeAdmin.html')

@sinLogin
def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("clave")
        
        api_url = f"http://localhost:8000/api/usuarios/login/"
        
        try:
            response = requests.post(api_url, 
                json={
                    'username': username,
                    'clave': password
                },
                headers={
                    'Content-Type': 'application/json',
                }
            )
            
            result = response.json()
            
            if result.get('success'):
                try:
                    user_rut = result['usuario']['rut']
                    django_user = User.objects.get(username=str(user_rut))
                    login(request, django_user)
                    
                    request.session['tokenApi'] = result.get('token')
                    
                    messages.success(request, f'Bienvenido {result["usuario"]["nombre"]}')
                    return redirect("/estacionamientos/")
                    
                except User.DoesNotExist:
                    messages.error(request, 'Error en la autenticación.')
            else:

                errors = result.get('errors', {})
                if 'non_field_errors' in errors:
                    messages.error(request, errors['non_field_errors'][0])
                else:
                    messages.error(request, 'Usuario o contraseña incorrectos.')
                    
        except requests.RequestException as e:
            messages.error(request, f'Error de conexión con la API: {str(e)}')

    return render(request, "login.html")

def logoutView(request):
    if 'tokenApi' in request.session:
        del request.session['tokenApi']
    
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return redirect("/login")
@sinLogin
def registroView(request):
    if request.method == "POST":
        formulario = RegistroClienteForm(request.POST)
        if formulario.is_valid():
            apiUrl = f"http://localhost:8000/api/usuarios/registro/"
            
            try:
                response = requests.post(apiUrl, 
                    json=formulario.cleaned_data,
                    headers={
                        'Content-Type': 'application/json',
                    }
                )
                
                result = response.json()
                
                if result.get('success'):
                    messages.success(request, f'¡Registro exitoso! Bienvenido {result["usuario"]["nombre"]}. Ya puedes iniciar sesión.')
                    return redirect("login")
                else:
                    for field, errors in result.get('errors', {}).items():
                        formulario.add_error(field, errors[0])
                    messages.error(request, 'Por favor corrige los errores del formulario.')
                        
            except requests.RequestException as e:
                messages.error(request, f'Error de conexión con la API: {str(e)}')
                
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        formulario = RegistroClienteForm()
    
    return render(request, "registro.html", {"form": formulario})

@loginRequerido
@soloAdminEmpleado
def crearUsuarios(request):
    if request.method == "POST":
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            apiUrl = f"http://localhost:8000/api/usuarios/"
            try:
                tokenApi = request.session.get('tokenApi')
                if not tokenApi:
                    messages.error(request, 'Token de autenticación no encontrado. Inicia sesión nuevamente.')
                    return redirect('login')
                
                datosApi = formulario.cleaned_data.copy()
                datosApi.pop('confirmar_clave', None)
                
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Token {tokenApi}"
                }
                
                response = requests.post(apiUrl,
                    json = datosApi,
                    headers = headers                  
                )
                result = response.json()

                if result.get("success"):
                    messages.success(request, 'Usuario creado.')
                    return redirect("listarUsuarios")
                else: 
                    for field, errors in result.get("error", {}).items():
                        formulario.add_error(field, errors[0])
            except requests.RequestException as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
    else:
        formulario = UsuarioForm()
    
    return render(request, "crear.html", {"form": formulario})

@loginRequerido
@soloAdminEmpleado
def listarUsuarios(request):
    apiUrl = "http://localhost:8000/api/usuarios/"
    
    try:
        response = requests.get(apiUrl, headers={
            'Content-Type': 'application/json',
        })
        
        result = response.json()
        
        if result.get("success"):
            usuarios = result.get("usuarios", [])
        else:
            usuarios = []
            messages.error(request, 'Error al cargar usuarios desde la API.')
            
    except requests.RequestException as e:
        usuarios = []
        messages.error(request, f'Error de conexión con la API: {str(e)}')
    
    return render(request, "listar.html", {"usuarios": usuarios})

@loginRequerido
@soloAdminEmpleado
def editarUsuario(request, rut):
    apiUrl = f"http://localhost:8000/api/usuarios/{rut}/"
    
    try:
        tokenApi = request.session.get('tokenApi')
        headers = {'Content-Type': 'application/json'}
        if tokenApi:
            headers['Authorization'] = f"Token {tokenApi}"
            
        response = requests.get(apiUrl, headers=headers)
        if response.status_code == 404:
            messages.error(request, 'Usuario no encontrado.')
            return redirect("listarUsuarios")
            
        usuario_data = response.json()
        
        if request.method == "POST":
            formulario = UsuarioForm(request.POST)
            if formulario.is_valid():
                try:
                    if not tokenApi:
                        messages.error(request, 'Token de autenticación no encontrado. Inicia sesión nuevamente.')
                        return redirect('login')
                    
                    datosApi = formulario.cleaned_data.copy()
                    datosApi.pop('confirmar_clave', None)
                    
                    update_response = requests.put(apiUrl,
                        json=datosApi,
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': f"Token {tokenApi}"
                        }
                    )
                    
                    result = update_response.json()
                    
                    if result.get("success"):
                        messages.success(request, f'Usuario {result["usuario"]["nombre"]} actualizado exitosamente.')
                        return redirect("listarUsuarios")
                    else:
                        for field, errors in result.get("errors", {}).items():
                            formulario.add_error(field, errors[0])
                        messages.error(request, 'Error al actualizar usuario.')
                        
                except requests.RequestException as e:
                    messages.error(request, f'Error de conexión con la API: {str(e)}')
            else:
                messages.error(request, 'Por favor corrige los errores del formulario.')
        else:
            formulario = UsuarioForm(initial=usuario_data)
    
    except requests.RequestException as e:
        messages.error(request, f'Error al cargar usuario: {str(e)}')
        return redirect("listarUsuarios")
    
    return render(request, "editar.html", {"form": formulario, "usuario": usuario_data})

@loginRequerido
@soloAdminEmpleado
def eliminarUsuario(request, rut):
    apiUrl = f"http://localhost:8000/api/usuarios/{rut}/"
    
    try:
        tokenApi = request.session.get('tokenApi')
        if not tokenApi:
            messages.error(request, 'Token de autenticación no encontrado. Inicia sesión nuevamente.')
            return redirect('login')
        
        response = requests.delete(apiUrl, headers={
            'Content-Type': 'application/json',
            'Authorization': f"Token {tokenApi}"
        })
        
        result = response.json()
        
        if result.get("success"):
            messages.success(request, f'Usuario eliminado exitosamente.')
        else:
            messages.error(request, 'Error al eliminar usuario.')
            
    except requests.RequestException as e:
        if "404" in str(e):
            messages.error(request, 'Usuario no encontrado.')
        else:
            messages.error(request, f'Error de conexión con la API: {str(e)}')
    
    return redirect("listarUsuarios")