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
from django.shortcuts import redirect
from apps.usuarios import views
from apps.usuarios.models import Usuario
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.usuarios.api import UsuarioViewSet
from apps.estacionamientos.api import EstacionamientoViewSet, ReservaViewSet, HistorialViewSet
from apps.empresas.api import EmpresaViewSet, SucursalViewSet
from apps.vehiculos.api import VehiculoViewSet


from apps.usuarios.views import homeCliente, homeAdmin

schema_view = get_schema_view(
    openapi.Info(
        title="Estacionamiento API",
        default_version='v1',
        description="API REST para el sistema de gestión de estacionamientos.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home(request):

    if request.user.is_authenticated:
        if hasattr(request.user, 'username') and request.user.username.isdigit():
            
            try:
                rut = int(request.user.username)
                usuario = Usuario.objects.get(rut=rut)
                if usuario.rol == 'Cliente':
                    return homeCliente(request)
            except Usuario.DoesNotExist:
                pass
        return homeAdmin(request)
    else:
        return redirect('login')
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'estacionamientos', EstacionamientoViewSet, basename='api-estacionamientos')
router.register(r'reservas', ReservaViewSet, basename='apiReservas')
router.register(r'historial', HistorialViewSet, basename='apiHistorial')
router.register(r'empresas', EmpresaViewSet, basename='apiEmpresas')
router.register(r'sucursales', SucursalViewSet, basename='apiSucursales')
router.register(r'vehiculos', VehiculoViewSet, basename='apiVehiculos')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),

    path("login/", views.loginView, name="login"), 
    path("logout/", views.logoutView, name="logout"),

    path("usuarios/", include("apps.usuarios.urls")),
    path("empresas/", include("apps.empresas.urls")),
    path("vehiculos/", include("apps.vehiculos.urls")),
    path("estacionamientos/", include("apps.estacionamientos.urls")),

    path("api/", include(router.urls)),

    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

