from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo
from .forms import VehiculoForm
from .serializers import VehiculoSerializer
from apps.utils.decoradores import loginRequerido  

@loginRequerido
def listar(solicitud):
    vehiculos = Vehiculo.objects.all().order_by("patente")
    return render(solicitud, "vehiculos/listar.html", {"vehiculos": vehiculos})

@loginRequerido
def crear(solicitud):
    if solicitud.method == "POST":
        serializador = VehiculoSerializer(data=solicitud.POST)
        if serializador.is_valid():
            serializador.save()
            return redirect("listarVehiculos")
        else:
            formulario = VehiculoForm(solicitud.POST)
            formulario.is_valid()
            for campo, errores in serializador.errors.items():
                for error in errores:
                    formulario.add_error(campo, error)
    else:
        formulario = VehiculoForm()
    return render(solicitud, "vehiculos/crear.html", {"form": formulario})

@loginRequerido
def editar(solicitud, id):
    vehiculo = get_object_or_404(Vehiculo, pk=id)

    if solicitud.method == "POST":
        serializador = VehiculoSerializer(vehiculo, data=solicitud.POST)
        if serializador.is_valid():
            serializador.save()
            return redirect("listarVehiculos")
        else:
            formulario = VehiculoForm(solicitud.POST, instance=vehiculo)
            formulario.is_valid()
            for campo, errores in serializador.errors.items():
                for error in errores:
                    formulario.add_error(campo, error)
    else:
        formulario = VehiculoForm(instance=vehiculo)

    return render(solicitud, "vehiculos/editar.html", {
        "form": formulario,
        "vehiculo": vehiculo
    })

@loginRequerido
def eliminar(solicitud, id):
    vehiculo = get_object_or_404(Vehiculo, pk=id)
    vehiculo.delete()
    return redirect("listarVehiculos")   

@loginRequerido
def eliminarTodos(solicitud):
    Vehiculo.objects.all().delete()
    return redirect("listarVehiculos")  
