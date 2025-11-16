from django.urls import path
from . import views

urlpatterns = [ 
    path("empresas/", views.listarEmpresa, name="empresas_listar"),
    path("empresas/crear/", views.gestionarEmpresa, name="empresas_crear"),# Definir ruta crearEmpresa
    path("empresas/<int:empresa_id>/editar/", views.gestionarEmpresa, name="empresas_editar"),# Definir ruta editarEmpresa
    path("empresas/<int:empresa_id>/eliminar/", views.eliminarEmpresa, name="empresas_eliminar"),# Definir ruta eliminarEmpresa
    
    path("empresas/<int:empresa_id>/sucursales/", views.listarSucursal, name="sucursales_listar"),
    path("empresas/<int:empresa_id>/sucursales/crear/", views.gestionarSucursal, name="sucursales_crear"),
    path("empresas/<int:empresa_id>/sucursales/<int:sucursal_id>/editar/", views.gestionarSucursal, name="sucursales_editar"),
    path("empresas/<int:empresa_id>/sucursales/<int:sucursal_id>/eliminar/", views.eliminarSucursal, name="sucursales_eliminar")
]