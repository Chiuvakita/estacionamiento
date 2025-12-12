from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
import requests

from apps.estacionamientos.forms.reservas import ReservaCrearForm
from apps.utils.decoradores import loginRequerido, soloCliente

API_BASE = "http://localhost:8000/api"


def _headers(request):
    token = request.session.get("tokenApi")
    if not token:
        return None
    return {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}",
    }


@loginRequerido
@soloCliente
def listarReserva(request):
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")

    data = []
    try:
        resp = requests.get(f"{API_BASE}/reservas/", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
        else:
            messages.error(request, "Error al cargar reservas desde la API.")
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")

    return render(request, "reserva/reservaListar.html", {"reservas": data})


@loginRequerido
@soloCliente
def crearReserva(request):
    error = None
    headers = _headers(request)
    if request.method == "POST":
        form = ReservaCrearForm(request.POST)
        if form.is_valid():
            vehiculo = form.cleaned_data["vehiculo"]
            est = form.cleaned_data["estacionamiento"]
            fecha_inicio = form.cleaned_data["fecha_inicio"]
            duracion_horas = form.cleaned_data["duracion"]

            if not headers:
                messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
                return redirect("login")
            try:
                payload = {
                    "vehiculo": vehiculo.id,
                    "estacionamiento": est.id,
                    "fechaInicio": fecha_inicio.isoformat(),
                    "duracionHoras": duracion_horas,
                }
                resp = requests.post(f"{API_BASE}/reservas/", json=payload, headers=headers)
                if resp.status_code in (200, 201):
                    messages.success(request, "Reserva creada.")
                    return redirect("listarReserva")
                errors = resp.json().get("errors") or resp.json()
                error = errors
            except requests.RequestException as e:
                messages.error(request, f"Error de conexión con la API: {e}")
    else:
        form = ReservaCrearForm()

    minimo = (timezone.localtime() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
    form.fields["fecha_inicio"].widget.attrs["min"] = minimo

    # estacionamientos disponibles desde API
    est_disponibles = []
    if headers:
        try:
            resp = requests.get(f"{API_BASE}/estacionamientos/", headers=headers)
            if resp.status_code == 200:
                est_disponibles = [e for e in resp.json() if e.get("estado") == "D"]
        except requests.RequestException:
            pass

    return render(request, "reserva/crearReserva.html", {
        "form": form,
        "estacionamientos": est_disponibles,
        "error": error
    })

@loginRequerido
@soloCliente
def terminarReserva(request, id):
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")
    try:
        resp = requests.post(f"{API_BASE}/reservas/{id}/terminar/", headers=headers)
        if resp.status_code in (200, 204):
            messages.success(request, "Reserva finalizada.")
        else:
            messages.error(request, f"No se pudo finalizar: {resp.json()}")
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")
    return redirect("listarReserva")
