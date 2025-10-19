from django.shortcuts import redirect
from django.conf import settings
from apps.usuarios.models import Usuario
from django.contrib import messages
from functools import wraps
def loginRequerido(funcion_vista):
    @wraps(funcion_vista)
    def verificar(request, *args, **kwargs):
        if request.user.is_authenticated:
            return funcion_vista(request, *args, **kwargs)
        else:
            return redirect(f"/login")
    return verificar

def sinLogin(funcion_vista):
    @wraps(funcion_vista)
    def verificar(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if request.user.username.isdigit():
                    rut = int(request.user.username)
                    usuario = Usuario.objects.get(rut=rut)
                    
                    if usuario.puedeGestionar():
                        return redirect('/estacionamientos/')
                    else: 
                        return redirect('/estacionamientos/')
                else:
                    return redirect('/usuarios/')
                    
            except (Usuario.DoesNotExist, ValueError):
                return redirect('/login/')
        else:
            return funcion_vista(request, *args, **kwargs)
    
    return verificar

def soloAdminEmpleado(funcion_vista):
    @wraps(funcion_vista)
    def verificar(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/login")
        
        try:
            if request.user.is_superuser:
                return funcion_vista(request, *args, **kwargs)
            
            if not request.user.username.isdigit():
                return redirect('/estacionamientos/reservas')
            
            rut = int(request.user.username)
            usuario = Usuario.objects.get(rut=rut)

            if usuario.puedeGestionar():
                return funcion_vista(request, *args, **kwargs)
            else:
                return redirect('/estacionamientos/reservas')
                
        except ValueError:
            return redirect('/estacionamientos/reservas')
        except Usuario.DoesNotExist:
            return redirect("/login/")   
    return verificar
