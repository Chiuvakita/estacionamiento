from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from .forms.usuarios import UsuarioForm

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

def listarUsuarios(request):
    usuariosList = Usuario.objects.all()
    return render(request, "listar.html", {"usuarios": usuariosList})

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
