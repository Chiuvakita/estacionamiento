from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from apps.empresas import forms
from apps.empresas.models import Empresa, Sucursal
from apps.empresas.serializers import EmpresaSerializer, SucursalSerializer
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado
from rest_framework import status


@loginRequerido
@soloAdminEmpleado
def gestionarEmpresa(request, empresa_id=None):
    if empresa_id:
        try:
            empresa = Empresa.objects.get(id=empresa_id)
        except Empresa.DoesNotExist:
            return HttpResponse("Empresa no encontrada", status=404)
    else:
        empresa = None
    
    if request.method == "POST":
        serializer = EmpresaSerializer(empresa, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect("empresas_listar")
        else:
            formulario = forms.EmpresaForm(request.POST, instance=empresa)
            formulario.is_valid()
            for field, errors in serializer.errors.items():
                for error in errors:
                    formulario.add_error(field, error)
    else:
        formulario = forms.EmpresaForm(instance=empresa)
        
    titulo = "Editar Empresa" if empresa_id else "Crear Empresa"
    datos = {'formulario': formulario, 'titulo': titulo}
    return render(request, "empresaForm.html", datos)

@loginRequerido
@soloAdminEmpleado
def listarEmpresa(request):
    empresas = Empresa.objects.all()
    return render(request, "empresaListar.html", {"empresas": empresas})


@loginRequerido
@soloAdminEmpleado
def eliminarEmpresa(request, empresa_id):
    try:
        empresa = Empresa.objects.get(id=empresa_id)
        if request.method == "POST":
            empresa.delete()
            return redirect("empresas_listar")
        return HttpResponse("Método erróneo", status=405)
    except Empresa.DoesNotExist:
        return HttpResponse("Empresa no encontrada", status=404)


@loginRequerido
@soloAdminEmpleado
def listarSucursal(request, empresa_id):
    try:
        empresa = Empresa.objects.get(id=empresa_id)
        sucursales = Sucursal.objects.filter(empresa_id=empresa_id)
        return render(request, "sucursalListar.html", {
            "sucursales": sucursales, 
            "empresa_id": empresa_id
        })
    except Empresa.DoesNotExist:
        return HttpResponse("Empresa no encontrada", status=404)


@loginRequerido
@soloAdminEmpleado
def gestionarSucursal(request, empresa_id, sucursal_id=None):
    try:
        empresa = Empresa.objects.get(id=empresa_id)
    except Empresa.DoesNotExist:
        return HttpResponse("Empresa no encontrada", status=404)
    
    if sucursal_id:
        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            return HttpResponse("Sucursal no encontrada", status=404)
    else:
        sucursal = None
    
    if request.method == "POST":
        data = request.POST.copy()
        data['empresa'] = empresa_id
        
        serializer = SucursalSerializer(sucursal, data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect("sucursales_listar", empresa_id=empresa_id)
        else:
            formulario = forms.SucursalForm(request.POST, instance=sucursal)
            formulario.is_valid()
            for field, errors in serializer.errors.items():
                if field != 'empresa':
                    for error in errors:
                        formulario.add_error(field, error)
    else:
        formulario = forms.SucursalForm(instance=sucursal)
        
    titulo = "Editar Sucursal" if sucursal_id else "Crear Sucursal"
    datos = {'formulario': formulario, 'titulo': titulo, "empresa_id": empresa_id}
    return render(request, "sucursalForm.html", datos)


@loginRequerido
@soloAdminEmpleado
def eliminarSucursal(request, empresa_id, sucursal_id):
    try:
        sucursal = Sucursal.objects.get(id=sucursal_id, empresa_id=empresa_id)
        if request.method == "POST":
            sucursal.delete()
            return redirect("sucursales_listar", empresa_id=empresa_id)
        return HttpResponse("Método erróneo", status=405)
    except Sucursal.DoesNotExist:
        return HttpResponse("Sucursal no encontrada", status=404)