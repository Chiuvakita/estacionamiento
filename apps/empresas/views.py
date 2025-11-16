from django.shortcuts import redirect, render
from django.http import HttpResponse
from apps.empresas import forms
from apps.empresas.models import Empresa,Sucursal
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado


@loginRequerido
@soloAdminEmpleado
def gestionarEmpresa(request, empresa_id=None):#funcion para crear y editar empresa
    
    if empresa_id:  # Si se proporciona un ID de empresa, estamos editando una empresa existente
        empresa = Empresa.objects.get(id=empresa_id)
    else:
        empresa = None  # Si no, estamos creando una nueva empresa
    
    if request.method == "POST": #Si el metodo es POST
        formulario = forms.EmpresaForm(request.POST, instance=empresa) #Se crea el formulario con los datos del POST y la instancia de empresa
        if formulario.is_valid(): #Si el formulario es valido
            formulario.save() #Se guarda el formulario
            return redirect("empresas_listar") #Se redirige a la lista de empresas
    else:
        formulario = forms.EmpresaForm(instance=empresa) ## Si es edición, formulario con datos; si es creación, formulario vacío
        
    titulo = "Editar Empresa" if empresa_id else "Crear Empresa"

    datos = {'formulario': formulario, 'titulo': titulo} #Se crea un diccionario con el formulario y el título
    return render(request, "empresaForm.html", datos) #Se renderiza con el diccionario
    
@loginRequerido
@soloAdminEmpleado
def listarEmpresa(request):
    empresas = Empresa.objects.all() #Se obtienen todas las empresas
    return render(request, "empresaListar.html", {"empresas": empresas}) #Y se pasan a la plantilla como lista de objetos

@loginRequerido
@soloAdminEmpleado
def eliminarEmpresa(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)  # Se obtiene la empresa que se va a eliminar
    if request.method == "POST":
        empresa.delete()  # Se elimina la empresa
        return redirect("empresas_listar")  # Llama a la vista de listarEmpresa para recargar la página
    return HttpResponse("Método erróneo")  # Si no es POST, retorna un error
    
    
@loginRequerido
@soloAdminEmpleado
def listarSucursal(request, empresa_id):
    sucursales = Sucursal.objects.filter(empresa_id=empresa_id) #Se obtienen todas las sucursales
    return render(request, "sucursalListar.html", {"sucursales": sucursales, "empresa_id": empresa_id}) #Y se pasan a la plantilla como lista de objetos

@loginRequerido
@soloAdminEmpleado
def gestionarSucursal(request, empresa_id, sucursal_id=None):#funcion para crear y editar sucursal
    
    if sucursal_id:  # Si se proporciona un ID de sucursal, estamos editando una sucursal existente
        sucursal = Sucursal.objects.get(id=sucursal_id)
    else:
        sucursal = None  # Si no, estamos creando una nueva sucursal
    
    if request.method == "POST": #Si el metodo es POST
        formulario = forms.SucursalForm(request.POST, instance=sucursal) #Se crea el formulario con los datos del POST y la instancia de sucursal
        if formulario.is_valid(): #Si el formulario es valido
            nuevaSucursal = formulario.save(commit=False) #Se crea el formulario, pero no se guarda
            nuevaSucursal.empresa_id = empresa_id
            nuevaSucursal.save() #Se guarda el formulario
            return redirect("sucursales_listar", empresa_id=empresa_id) #Se redirige a la lista de sucursales
    else:
        formulario = forms.SucursalForm(instance=sucursal) ## Si es edición, formulario con datos; si es creación, formulario vacío
        
    titulo = "Editar Sucursal" if sucursal_id else "Crear Sucursal"

    datos = {'formulario': formulario, 'titulo': titulo, "empresa_id": empresa_id} #Se crea un diccionario con el formulario y el título
    return render(request, "sucursalForm.html", datos) #Se renderiza con el diccionario

@loginRequerido
@soloAdminEmpleado
def eliminarSucursal(request, empresa_id, sucursal_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)  # Se obtiene la sucursal que se va a eliminar
    if request.method == "POST":
        sucursal.delete()  # Se elimina la sucursal
        return redirect("sucursales_listar", empresa_id=empresa_id)  # Llama a la vista de listarSucursal para recargar la página
    return HttpResponse("Método erróneo")  # Si no es POST, retorna un error