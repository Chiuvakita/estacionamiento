from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models.estacionamiento import Estacionamiento
from .services import ocupar_estacionamiento, liberar_estacionamiento

def home(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        modo = request.POST.get("modo")

        if modo == "especifico":
            est_id = int(request.POST.get("estacionamiento_id"))
            estacionamiento = Estacionamiento.objects.filter(pk=est_id, estado="D").first()
        else:
            estacionamiento = Estacionamiento.objects.filter(estado="D").first()

        if estacionamiento:
            ocupar_estacionamiento(estacionamiento, patente, es_reserva=False)

        return redirect("home")

    disponibles = Estacionamiento.objects.filter(estado="D").count()
    ocupados = Estacionamiento.objects.filter(estado="O")
    estacionamientos = Estacionamiento.objects.all().order_by("id")

    return render(request, "main/home.html", {
        "disponibles": disponibles,
        "ocupados": ocupados,
        "estacionamientos": estacionamientos
    })

def marcarSalida(request, id):
    est = get_object_or_404(Estacionamiento, pk=id)
    liberar_estacionamiento(est)
    return redirect("home")

def marcarSalidaPatente(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        est = Estacionamiento.objects.filter(patente=patente).first()
        if est:
            liberar_estacionamiento(est)
    return redirect("home")
