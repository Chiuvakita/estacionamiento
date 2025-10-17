from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models.estacionamiento import Estacionamiento
from ..forms.reservas import ReservaCrearForm, Reserva
from .services import ocupar_estacionamiento, liberar_estacionamiento, existe_reserva_activa_o_programada

def listarReserva(request):
    data = []
    ahora = timezone.now()

    for r in Reserva.objects.order_by("-id"):
        duracion = 0
        if r.fecha_inicio and r.fecha_termino:
            duracion = (r.fecha_termino - r.fecha_inicio).total_seconds() / 3600
        duracion_str = f"{int(duracion)} horas" if duracion else "-"

        if r.fecha_termino and r.fecha_termino > ahora:
            diff = r.fecha_termino - ahora
            horas = diff.seconds // 3600
            minutos = (diff.seconds % 3600) // 60
            tiempo_restante = f"{horas}h {minutos}m"
        else:
            tiempo_restante = "Finalizada"

        data.append({
            "id": r.id,
            "patente": r.patente,
            "estacionamiento_id": r.estacionamiento_id,
            "fechaInicio": r.fecha_inicio.strftime("%Y-%m-%d %H:%M"),
            "fechaTermino": r.fecha_termino.strftime("%Y-%m-%d %H:%M") if r.fecha_termino else "-",
            "duracion": duracion_str,
            "tiempoRestante": tiempo_restante
        })

    return render(request, "reserva/reservaListar.html", {"reservas": data})

def crearReserva(request):
    if request.method == "POST":
        form = ReservaCrearForm(request.POST)
        if form.is_valid():
            patente = form.cleaned_data["patente"]
            fecha_inicio = form.cleaned_data["fecha_inicio"]
            duracion_horas = form.cleaned_data["duracion"]
            fecha_termino = fecha_inicio + timedelta(hours=duracion_horas)

            est_id = form.cleaned_data["estacionamiento_id"]
            est = Estacionamiento.objects.filter(pk=est_id).first()  # ✅ Correcto

            if existe_reserva_activa_o_programada():
                return render(request, "reserva/crearReserva.html", {
                    "form": form,
                    "estacionamientos": Estacionamiento.objects.filter(estado="D"),
                    "error": "Ya existe una reserva activa o programada. Debe finalizar antes de crear otra."
                })

            if est and est.estado == "D":
                Reserva.objects.create(
                    estacionamiento_id=est.id,  
                    patente=patente,
                    fecha_inicio=fecha_inicio,
                    fecha_termino=fecha_termino
                )
                ocupar_estacionamiento(est, patente, fecha_inicio, fecha_termino, es_reserva=True)

            return redirect("listarReserva")
    else:
        form = ReservaCrearForm()

    est_disponibles = Estacionamiento.objects.filter(estado="D").order_by("id")
    return render(request, "reserva/crearReserva.html", {
        "form": form,
        "estacionamientos": est_disponibles
    })

def terminarReserva(request, id):
    r = get_object_or_404(Reserva, pk=id)

    est = Estacionamiento.objects.filter(id=r.estacionamiento_id).first()

    if est:
        liberar_estacionamiento(est)

    r.fecha_termino = timezone.now()
    r.save()

    return redirect("listarReserva")
