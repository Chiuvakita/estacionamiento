from django.shortcuts import render, redirect, get_object_or_404
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
        Reserva.objects.all().delete()
        Estacionamiento.objects.all().delete()
        Historial.objects.all().delete()
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEliminarTodos.html")

@loginRequerido
@soloAdminEmpleado
def eliminarEstacionamiento(request, id):
    est = get_object_or_404(Estacionamiento, pk=id)
    if request.method == "POST":
        est.delete()
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEliminar.html", {"id": id})
