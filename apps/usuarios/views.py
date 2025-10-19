from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from .models import Usuario
from .forms.usuarios import UsuarioForm
from apps.utils.decoradores import loginRequerido, sinLogin, soloAdminEmpleado


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
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/estacionamientos/")
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, "login.html")

def logoutView(request):
    logout(request)
    messages.success(request, 'Sesión cerrada')
    return redirect("/login")


@loginRequerido
@soloAdminEmpleado
def crearUsuarios(request):
    if request.method == "POST":
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            try:
                usuario = formulario.save()
                messages.success(request, f'Usuario {usuario.nombre} {usuario.apellidoPaterno} creado exitosamente.')
                return redirect("listarUsuarios")
            except Exception as excepcion:
                messages.error(request, f'Error al crear usuario: {str(excepcion)}')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        formulario = UsuarioForm()
    
    return render(request, "crear.html", {"form": formulario})

@loginRequerido
@soloAdminEmpleado
def listarUsuarios(request):
    usuariosList = Usuario.objects.all()
    return render(request, "listar.html", {"usuarios": usuariosList})

@loginRequerido
@soloAdminEmpleado
def editarUsuario(request, rut):
    try:
        usuario = Usuario.objects.get(rut=rut)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect("listarUsuarios")
    
    if request.method == "POST":
        formulario = UsuarioForm(request.POST, instance=usuario, rutReadonly=True)
        if formulario.is_valid():
            try:
                usuarioActualizado = formulario.save()
                messages.success(request, f'Usuario {usuarioActualizado.nombre} {usuarioActualizado.apellidoPaterno} actualizado exitosamente.')
                return redirect("listarUsuarios")
            except Exception as excepcion:
                messages.error(request, f'Error al actualizar usuario: {str(excepcion)}')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        formulario = UsuarioForm(instance=usuario, rutReadonly=True)
    
    return render(request, "editar.html", {"form": formulario, "usuario": usuario})

@loginRequerido
@soloAdminEmpleado
def eliminarUsuario(request, rut):
    try:
        usuario = Usuario.objects.get(rut=rut)
        nombreCompleto = f"{usuario.nombre} {usuario.apellidoPaterno}"
        usuario.delete()
        messages.success(request, f'Usuario {nombreCompleto} eliminado exitosamente.')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
    except Exception as excepcion:
        messages.error(request, f'Error al eliminar usuario: {str(excepcion)}')
    
    return redirect("listarUsuarios")
