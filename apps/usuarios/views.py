from django.shortcuts import render, redirect
from .models import Usuario

def crearUsuarios(request):
    if request.method == "POST":
        rut=request.POST["rut"]
        nombre=request.POST["nombre"]
        apellidoPaterno=request.POST["apellidoPaterno"]
        apellidoMaterno=request.POST["apellidoMaterno"]
        numeroTelefono=request.POST["numeroTelefono"]
        rol=request.POST["rol"]
        discapacidad = request.POST.get("discapacidad") == "true"
        
        Usuario.objects.create(
            rut=rut,
            nombre=nombre, 
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            numeroTelefono=numeroTelefono,
            rol=rol,
            discapacidad=discapacidad
        )
        return redirect("listarUsuarios")
    return render(request, "crear.html")

def listarUsuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "listar.html", {"usuarios": usuarios})

def editarUsuario(request, rut):
    usuario = Usuario.objects.get(rut=rut)
    if request.method == "POST":
        usuario.rut = request.POST["rut"]
        usuario.nombre = request.POST["nombre"]
        usuario.apellidoPaterno = request.POST["apellidoPaterno"]
        usuario.apellidoMaterno = request.POST["apellidoMaterno"]
        usuario.numeroTelefono = request.POST["numeroTelefono"]
        usuario.rol = request.POST["rol"]
        usuario.discapacidad = "discapacidad" in request.POST
        usuario.save()
        return redirect("listarUsuarios")
    return render(request, "editar.html", {"usuario": usuario})

def eliminarUsuario(request, rut):
    usuario = Usuario.objects.get(rut=rut)
    usuario.delete()
    return redirect("listarUsuarios")
