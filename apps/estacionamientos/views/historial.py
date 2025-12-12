from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado

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
@soloAdminEmpleado
def listarHistorial(request):
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")

    historial = []
    try:
        resp = requests.get(f"{API_BASE}/historial/", headers=headers)
        if resp.status_code == 200:
            historial = resp.json()
        else:
            messages.error(request, "Error al cargar historial desde la API.")
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")

    total_registros = len(historial)
    total_reservas = sum(1 for h in historial if h.get("es_reserva"))
    total_estacionamientos = len(set(h.get("estacionamiento") for h in historial if h.get("estacionamiento") is not None))

    return render(request, "historial/historialListar.html", {
        "historial": historial,
        "total_reservas": total_reservas,
        "total_registros": total_registros,
        "total_estacionamientos": total_estacionamientos
    })
