from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Estacionamiento, Reserva, Historial
from .forms import EstacionamientoForm, EstacionamientosMasivoForm, ReservaCrearForm


# ===========================
# HOME (principal)
# ===========================
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
            estacionamiento.estado = "O"
            estacionamiento.patente = patente
            estacionamiento.fecha_inicio = timezone.now()
            estacionamiento.fecha_termino = None
            estacionamiento.save()

            Historial.objects.create(
                estacionamiento=estacionamiento,
                patente=patente,
                fecha_inicio=estacionamiento.fecha_inicio,
                es_reserva=False
            )

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
    est.estado = "D"
    est.patente = None
    est.fecha_termino = timezone.now()
    est.save()

    mov = Historial.objects.filter(estacionamiento=est, fecha_termino__isnull=True).last()
    if mov:
        mov.fecha_termino = est.fecha_termino
        mov.save()

    return redirect("home")


def marcarSalidaPatente(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        est = Estacionamiento.objects.filter(patente=patente).first()
        if est:
            est.estado = "D"
            est.patente = None
            est.fecha_termino = timezone.now()
            est.save()

            mov = Historial.objects.filter(estacionamiento=est, fecha_termino__isnull=True).last()
            if mov:
                mov.fecha_termino = est.fecha_termino
                mov.save()

    return redirect("home")


# ===========================
# ESTACIONAMIENTOS (CRUD)
# ===========================
def listarEstacionamiento(request):
    qs = Estacionamiento.objects.all().order_by("id")
    return render(request, "estacionamiento/estacionamientoListar.html", {"estacionamientos": qs})


def crearEstacionamiento(request):
    if request.method == "POST":
        form = EstacionamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listarEstacionamiento")
    else:
        form = EstacionamientoForm()
    return render(request, "estacionamiento/estacionamientoCrear.html", {"form": form})


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


def eliminarTodosEstacionamientos(request):
    if request.method == "POST":
        Reserva.objects.all().delete()
        Estacionamiento.objects.all().delete()
        Historial.objects.all().delete()  
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEliminarTodos.html")


def eliminarEstacionamiento(request, id):
    est = get_object_or_404(Estacionamiento, pk=id)
    if request.method == "POST":
        est.delete()
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEliminar.html", {"id": id})


# ===========================
# RESERVAS (cliente)
# ===========================
def listarReserva(request):
    data = []
    ahora = timezone.now()

    for r in Reserva.objects.select_related("estacionamiento").order_by("-id"):
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
            est = Estacionamiento.objects.filter(pk=est_id).first()


            reserva_activa = Reserva.objects.filter(
                fecha_termino__isnull=True
            ) | Reserva.objects.filter(
                fecha_termino__gt=timezone.now()
            )

            if reserva_activa.exists():
                return render(request, "reserva/crearReserva.html", {
                    "form": form,
                    "estacionamientos": Estacionamiento.objects.filter(estado="D"),
                    "error": "Ya existe una reserva activa o programada. Debe finalizar antes de crear otra."
                })

            if est and est.estado == "D":
                Reserva.objects.create(
                    estacionamiento=est,
                    patente=patente,
                    fecha_inicio=fecha_inicio,
                    fecha_termino=fecha_termino,
                    tipo_snapshot=est.tipo,
                )
                est.estado = "O"
                est.patente = patente
                est.fecha_inicio = fecha_inicio
                est.fecha_termino = fecha_termino
                est.save()

                Historial.objects.create(
                    estacionamiento=est,
                    patente=patente,
                    fecha_inicio=fecha_inicio,
                    fecha_termino=fecha_termino,
                    es_reserva=True
                )

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
    est = r.estacionamiento
    est.estado = "D"
    est.patente = None
    est.fecha_termino = timezone.now()
    est.save()
    r.fecha_termino = timezone.now()
    r.save()

    mov = Historial.objects.filter(estacionamiento=est, fecha_termino__isnull=True).last()
    if mov:
        mov.fecha_termino = est.fecha_termino
        mov.save()

    return redirect("listarReserva")


# ===========================
# HISTORIAL
# ===========================
def listarHistorial(request):
    historial = Historial.objects.all().order_by("estacionamiento_id", "-fecha_inicio")
    total_reservas = historial.filter(es_reserva=True).count()
    return render(request, "historial/historialListar.html", {
        "historial": historial,
        "total_reservas": total_reservas
    })
