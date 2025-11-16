from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from apps.estacionamientos.models.estacionamiento import Estacionamiento
from apps.estacionamientos.models.reserva import Reserva
from apps.estacionamientos.forms.reservas import ReservaCrearForm
from apps.estacionamientos.views.services import (
    ocupar_estacionamiento,
    liberar_estacionamiento,
    existe_reserva_activa_o_programada,
)
from apps.utils.decoradores import loginRequerido, soloCliente


@loginRequerido
@soloCliente
def listarReserva(request):
    data = []
    ahora = timezone.now()

    for r in Reserva.objects.select_related("vehiculo", "estacionamiento").order_by("-id"):
        if r.fecha_inicio and r.fecha_termino:
            duracion = (r.fecha_termino - r.fecha_inicio).total_seconds() / 3600
        else:
            duracion = 0
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
            "patente": r.vehiculo.patente,
            "estacionamiento_id": r.estacionamiento.id,
            "fechaInicio": r.fecha_inicio.strftime("%Y-%m-%d %H:%M"),
            "fechaTermino": r.fecha_termino.strftime("%Y-%m-%d %H:%M") if r.fecha_termino else "-",
            "duracion": duracion_str,
            "tiempoRestante": tiempo_restante,
        })

    return render(request, "reserva/reservaListar.html", {"reservas": data})


@loginRequerido
@soloCliente
def crearReserva(request):
    error = None

    if request.method == "POST":
        form = ReservaCrearForm(request.POST)
        if form.is_valid():
            vehiculo = form.cleaned_data["vehiculo"]
            est = form.cleaned_data["estacionamiento"]
            fecha_inicio = form.cleaned_data["fecha_inicio"]
            duracion_horas = form.cleaned_data["duracion"]
            fecha_termino = fecha_inicio + timedelta(hours=duracion_horas)

            if existe_reserva_activa_o_programada():
                error = "Ya existe una reserva activa o programada. Finalízala antes de crear otra."

            elif est.estado == "D":

                Reserva.objects.create(
                    estacionamiento=est,
                    vehiculo=vehiculo,
                    fecha_inicio=fecha_inicio,
                    fecha_termino=fecha_termino,
                    tipo_snapshot=est.tipo
                )

                ocupar_estacionamiento(
                    est=est,
                    patente=vehiculo.patente,
                    fecha_inicio=fecha_inicio,
                    es_reserva=True
                )

                return redirect("listarReserva")
            else:
                error = "El estacionamiento no está disponible."
    else:
        form = ReservaCrearForm()

    minimo = (timezone.localtime() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
    form.fields["fecha_inicio"].widget.attrs["min"] = minimo

    est_disponibles = Estacionamiento.objects.filter(estado="D").order_by("id")

    return render(request, "reserva/crearReserva.html", {
        "form": form,
        "estacionamientos": est_disponibles,
        "error": error
    })

@loginRequerido
@soloCliente
def terminarReserva(request, id):
    r = get_object_or_404(Reserva, pk=id)

    est = r.estacionamiento

    if est:
        liberar_estacionamiento(est)

    r.fecha_termino = timezone.now()
    r.save()

    return redirect("listarReserva")
