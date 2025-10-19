from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo
from .forms import VehiculoForm

def listarVehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/listar.html', {'vehiculos': vehiculos})

def crearVehiculo(request):
    error = None
    form = VehiculoForm(request.POST or None)

    if request.method == "POST":
        # Limitar a 3 vehículos
        if Vehiculo.objects.count() >= 3:
            error = "Solo puedes registrar un máximo de 3 vehículos."
        elif form.is_valid():
            try:
                form.save()
                return redirect('listarVehiculos')
            except:
                error = "Ya existe un vehículo con esa patente."

    return render(request, 'vehiculos/crear.html', {'form': form, 'error': error})

def editarVehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    form = VehiculoForm(request.POST or None, instance=vehiculo)
    if form.is_valid():
        form.save()
        return redirect('listarVehiculos')
    return render(request, 'vehiculos/editar.html', {'form': form})

def eliminarVehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    return redirect('listarVehiculos')

def eliminarTodosVehiculos(request):
    Vehiculo.objects.all().delete()
    return redirect('listarVehiculos')
