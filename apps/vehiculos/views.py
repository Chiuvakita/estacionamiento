from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo
from .forms import VehiculoForm
from apps.utils.decoradores import loginRequerido  

@loginRequerido
def listar(request):
    vehiculos = Vehiculo.objects.all().order_by("patente")
    return render(request, "vehiculos/listar.html", {"vehiculos": vehiculos})

@loginRequerido
def crear(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarVehiculos")   
    else:
        form = VehiculoForm()
    return render(request, "vehiculos/crear.html", {"form": form})

@loginRequerido
def editar(request, id):
    vehiculo = get_object_or_404(Vehiculo, pk=id)

    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect("listarVehiculos")   
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, "vehiculos/editar.html", {
        "form": form,
        "vehiculo": vehiculo
    })

@loginRequerido
def eliminar(request, id):
    vehiculo = get_object_or_404(Vehiculo, pk=id)
    vehiculo.delete()
    return redirect("listarVehiculos")   

@loginRequerido
def eliminar_todos(request):
    Vehiculo.objects.all().delete()
    return redirect("listarVehiculos")  
