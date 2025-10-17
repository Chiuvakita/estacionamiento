from django.shortcuts import redirect
from django.conf import settings
from .models import Usuario
from django.contrib import messages
def loginRequerido(funcion_vista):
    def verificar(request, *args, **kwargs):
        if request.user.is_authenticated:
            return funcion_vista(request, *args, **kwargs)
        else:
            redireccion = request.get_full_path()
            return redirect(f"{settings.RUTA_LOGIN}?next={redireccion}")
    return verificar

def sinLogin(funcion_vista):
    def verificar(request, *args, **kwargs):
        if request.user.is_authenticated:
            redireccion = request.get_full_path()
            return redirect(f"{settings.RUTA_DESPUES_LOGIN}?next={redireccion}")
        else:
            return funcion_vista(request, *args, **kwargs)
    return verificar

def soloAdminEmpleado(funcion_vista):
    def verificar(request, *args, **kwargs):
        if not request.user.is_authenticated:
            redireccion = request.get_full_path()
            return redirect(f"{settings.RUTA_LOGIN}?next={redireccion}")
        try:
            usuario = Usuario.objects.get(rut=request.user.username)

            if usuario.puedeGestionar():
                return funcion_vista(request, *args, **kwargs)
            else:
                messages.error(request, "No tienes permiso para acceder a esta pagina")
                return redirect(settings.RUTA_DESPUES_LOGIN)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return redirect(settings.RUTA_LOGIN)
    return verificar

