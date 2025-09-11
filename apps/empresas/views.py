from django.shortcuts import render
from django.http import HttpResponse
from apps.empresas.models import Empresa,Sucursal

# Create your views here.
def listar_empresas(request):
    return render(request, "empresaListar.html")
      
# Realizar crearEmpresa
def crearEmpresa(request, empresa=None):
    if request.method == "POST": #Si el metodo es POST
    
        empresa = Empresa.objects.create( #Se crea la empresa con los valores del formulario
            nombre=request.POST.get("nombre"),
            telefono=request.POST.get("telefono"),
            correo=request.POST.get("correo"),
            direccion=request.POST.get("direccion")
        )
        return render(request,"empresaCreada.html",{"empresa": empresa}) #Y se retorna la página de empresa creada, incluyendo la empresa como objeto
    return render(request, "empresaForm.html") #Si es GET, se muestra el formulario
    
# Realizar listarEmpresa
def listarEmpresa(request):
    empresas = Empresa.objects.all() #Se obtienen todas las empresas
    return render(request, "empresaListar.html", {"empresas": empresas}) #Y se pasan a la plantilla como lista de objetos

# Realizar editarEmpresa
def editarEmpresa(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)  # Se obtiene la empresa a editar por su id
    if request.method == "POST":
        empresa.nombre = request.POST.get("nombre")
        empresa.telefono = request.POST.get("telefono")
        empresa.correo = request.POST.get("correo")
        empresa.direccion = request.POST.get("direccion")
        empresa.save()
        return render(request, "empresaEditar.html", {"empresa": empresa})  # Redirige al formulario de edición con los datos actualizados
    return render(request, "empresaEditar.html", {"empresa": empresa})  # Si es GET, muestra el formulario de edición con los datos actuales

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
