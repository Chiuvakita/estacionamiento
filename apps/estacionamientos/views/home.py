from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models.estacionamiento import Estacionamiento
from .services import ocupar_estacionamiento, liberar_estacionamiento
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado


@loginRequerido
@soloAdminEmpleado
def home(request):
    if request.method == "POST":
        patente = request.POST.get("patente", "").strip().upper()
        modo = request.POST.get("modo")

        if modo == "especifico":
            est_id = request.POST.get("estacionamiento_id")
            estacionamiento = (
                Estacionamiento.objects.filter(pk=est_id, estado="D").first()
            )
        else:
            estacionamiento = Estacionamiento.objects.filter(estado="D").first()

        if estacionamiento:
            ocupar_estacionamiento(estacionamiento, patente)
        else:
            print("No hay estacionamientos disponibles para ocupar")

        return redirect("home")

    disponibles = Estacionamiento.objects.filter(estado="D").count()
    ocupados = Estacionamiento.objects.filter(estado="O")
    estacionamientos = Estacionamiento.objects.all().order_by("id")

    return render(
        request,
        "homeAdmin.html",
        {
            "disponibles": disponibles,
            "ocupados": ocupados,
            "estacionamientos": estacionamientos,
        },
    )


@loginRequerido
@soloAdminEmpleado
def marcarSalida(request, id):
    est = get_object_or_404(Estacionamiento, pk=id)
    liberar_estacionamiento(est)
    return redirect("home")

@loginRequerido
@soloAdminEmpleado
def marcarSalidaPatente(request):
    if request.method == "POST":
        patente = request.POST.get("patente", "").strip().upper()
        est = Estacionamiento.objects.filter(patente=patente, estado="O").first()
        if est:
            liberar_estacionamiento(est)
    return redirect("home")
