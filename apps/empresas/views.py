from django.shortcuts import redirect, render
from django.http import HttpResponse
from apps.empresas.models import Empresa,Sucursal
from . import forms

# Realizar gestionarEmpresa
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
    
# Realizar listarEmpresa
def listarEmpresa(request):
    empresas = Empresa.objects.all() #Se obtienen todas las empresas
    return render(request, "empresaListar.html", {"empresas": empresas}) #Y se pasan a la plantilla como lista de objetos

# Realizar eliminarEmpresa
def eliminarEmpresa(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)  # Se obtiene la empresa que se va a eliminar
    if request.method == "POST":
        empresa.delete()  # Se elimina la empresa
        return listarEmpresa(request)  # Llama a la vista de listarEmpresa para recargar la página
    return HttpResponse("Método erróneo")  # Si no es POST, retorna un error
    
    
# Realizar listarSucursal
# Realizar crearSucursal
# Realizar editarSucursal
# Realizar eliminarSucursal

# Realizar asociarUsuarioSucursal
