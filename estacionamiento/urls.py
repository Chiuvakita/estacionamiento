"""
URL configuration for estacionamiento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from apps.usuarios import views
from apps.usuarios.models import Usuario

from apps.usuarios.views import homeCliente, homeAdmin

def home(request):
    if request.user.is_authenticated:
        # Si es cliente
        if hasattr(request.user, 'username') and request.user.username.isdigit():
            
            try:
                rut = int(request.user.username)
                usuario = Usuario.objects.get(rut=rut)
                if usuario.rol == 'Cliente':
                    return homeCliente(request)
            except Usuario.DoesNotExist:
                pass
        # Si es admin o empleado
        return homeAdmin(request)
    else:
        return redirect('login')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),

    path("login/", views.loginView, name="login"), 
    path("logout/", views.logoutView, name="logout"),

    path("usuarios/", include("apps.usuarios.urls")),
    path("empresas/", include("apps.empresas.urls")),
    path("vehiculos/", include("apps.vehiculos.urls")),
    path("estacionamientos/", include("apps.estacionamientos.urls")),

]






# TODO: Conectar todas las rutas de cada app aquí
# path("usuarios/", include("apps.usuarios.urls"))
# path("empresas/", include("apps.empresas.urls"))
# path("vehiculos/", include("apps.vehiculos.urls"))
# path("estacionamientos/", include("apps.estacionamientos.urls"))
