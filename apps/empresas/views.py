from django.shortcuts import render
from django.http import HttpResponse
from apps.empresas.models import Empresa,Sucursal

# Create your views here.
def listar_empresas(request):
    return render(request, "empresaListar.html")
    
    
# Realizar crearEmpresa
def crearEmpresa(request):
    empresa = Empresa.objects.create(
        nombre = "Estacionamiento inacap",
        telefono = "+56966774563",
        correo = "example@inacapmail.cl",
        direccion = "Yumbel 468"
    )
    return HttpResponse(f"Empresa creada: {empresa.nombre}")


# Realizar listarEmpresa
def listarEmpresa(request):
    empresas = Empresa.objects.all()
    respuesta = """
    <table>
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Teléfono</th>
                <th>Correo</th>
                <th>Dirección</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for e in empresas:
        respuesta += f"""
        <tr>
            <td>{e.nombre}</td>
            <td>{e.telefono}</td>
            <td>{e.correo}</td>
            <td>{e.direccion}</td>
        </tr>
        """
    
    respuesta += "</tbody></table>"
    return HttpResponse(respuesta)

# Realizar editarEmpresa
# Realizar eliminarEmpresa

# Realizar listarSucursal
# Realizar crearSucursal
# Realizar editarSucursal
# Realizar eliminarSucursal

# Realizar asociarUsuarioSucursal
