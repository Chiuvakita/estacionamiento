from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import EmpresaViewSet, SucursalViewSet

enrutador = DefaultRouter()
enrutador.register(r'api/empresas', EmpresaViewSet, basename='empresa')
enrutador.register(r'api/sucursales', SucursalViewSet, basename='sucursal')

urlpatterns = [ 
    path("empresas/", views.listarEmpresa, name="empresas_listar"),
    path("empresas/crear/", views.gestionarEmpresa, name="empresas_crear"),
    path("empresas/<int:empresaId>/editar/", views.gestionarEmpresa, name="empresas_editar"),
    path("empresas/<int:empresaId>/eliminar/", views.eliminarEmpresa, name="empresas_eliminar"),
    
    path("empresas/<int:empresaId>/sucursales/", views.listarSucursal, name="sucursales_listar"),
    path("empresas/<int:empresaId>/sucursales/crear/", views.gestionarSucursal, name="sucursales_crear"),
    path("empresas/<int:empresaId>/sucursales/<int:sucursalId>/editar/", views.gestionarSucursal, name="sucursales_editar"),
    path("empresas/<int:empresaId>/sucursales/<int:sucursalId>/eliminar/", views.eliminarSucursal, name="sucursales_eliminar"),
    
    path('', include(enrutador.urls)),
]