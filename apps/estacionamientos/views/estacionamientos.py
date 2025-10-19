from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from ..models.estacionamiento import Estacionamiento
from ..models.reserva import Reserva
from ..models.historial import Historial
from ..forms.estacionamientos import EstacionamientoForm, EstacionamientosMasivoForm
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado

@loginRequerido
@soloAdminEmpleado
def listarEstacionamiento(request):
    qs = Estacionamiento.objects.all().order_by("id")
    return render(request, "estacionamiento/estacionamientoListar.html", {"estacionamientos": qs})

@loginRequerido
@soloAdminEmpleado
def crearEstacionamiento(request):
    if request.method == "POST":
        form = EstacionamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarEstacionamiento")
    else:
        form = EstacionamientoForm()
    return render(request, "estacionamiento/estacionamientoCrear.html", {"form": form})

@loginRequerido
@soloAdminEmpleado
def crearEstacionamientosMasivo(request):
    if request.method == "POST":
        form = EstacionamientosMasivoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]
            tipo = form.cleaned_data["tipo"]
            objs = [Estacionamiento(estado="D", tipo=tipo) for _ in range(cantidad)]
            Estacionamiento.objects.bulk_create(objs)
            return redirect("listarEstacionamiento")
    else:
        form = EstacionamientosMasivoForm()
    return render(request, "estacionamiento/estacionamientoCrearMasivo.html", {"form": form})

@loginRequerido
@soloAdminEmpleado
def editarEstacionamiento(request, id):
    est = get_object_or_404(Estacionamiento, pk=id)
    if request.method == "POST":
        form = EstacionamientoForm(request.POST, instance=est)
        if form.is_valid():
            form.save()
            return redirect("listarEstacionamiento")
    else:
        form = EstacionamientoForm(instance=est)
    return render(request, "estacionamiento/estacionamientoEditar.html", {"form": form, "id": id})

@loginRequerido
@soloAdminEmpleado
def eliminarTodosEstacionamientos(request):
    if request.method == "POST":
        Estacionamiento.objects.all().delete()
        Reserva.objects.all().delete()
        Historial.objects.all().delete()

        return redirect("listarEstacionamiento")

    return redirect("listarEstacionamiento")


@loginRequerido
@soloAdminEmpleado
def eliminarEstacionamiento(request, id):
    if request.method == "POST":
        est = get_object_or_404(Estacionamiento, pk=id)
        est.delete()
        return redirect("listarEstacionamiento")

    return redirect("listarEstacionamiento")
