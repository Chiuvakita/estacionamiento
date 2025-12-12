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
def home(request):
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")

    if request.method == "POST":
        patente = request.POST.get("patente", "").strip().upper()
        modo = request.POST.get("modo")

        try:
            resp_list = requests.get(f"{API_BASE}/estacionamientos/", headers=headers)
            if resp_list.status_code != 200:
                messages.error(request, "No se pudieron obtener estacionamientos.")
                return redirect("home")
            ests = resp_list.json()
        except requests.RequestException as e:
            messages.error(request, f"Error de conexión con la API: {e}")
            return redirect("home")

        est_target = None
        if modo == "especifico":
            est_id = request.POST.get("estacionamiento_id")
            est_target = next((e for e in ests if str(e.get("id")) == str(est_id) and e.get("estado") == "D"), None)
        else:
            est_target = next((e for e in ests if e.get("estado") == "D"), None)

        if est_target:
            try:
                requests.post(
                    f"{API_BASE}/estacionamientos/{est_target['id']}/ocupar/",
                    json={"patente": patente},
                    headers=headers,
                )
                messages.success(request, "Estacionamiento ocupado.")
            except requests.RequestException as e:
                messages.error(request, f"Error de conexión con la API: {e}")
        else:
            messages.error(request, "No hay estacionamientos disponibles para ocupar")

        return redirect("home")

    try:
        resp = requests.get(f"{API_BASE}/estacionamientos/", headers=headers)
        if resp.status_code != 200:
            messages.error(request, "No se pudieron obtener estacionamientos.")
            return redirect("login")
        estacionamientos = resp.json()
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")
        return redirect("login")

    disponibles = sum(1 for e in estacionamientos if e.get("estado") == "D")
    ocupados = [e for e in estacionamientos if e.get("estado") == "O"]

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
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")
    try:
        requests.post(f"{API_BASE}/estacionamientos/{id}/liberar/", headers=headers)
        messages.success(request, "Salida registrada.")
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")
    return redirect("home")

@loginRequerido
@soloAdminEmpleado
def marcarSalidaPatente(request):
    if request.method == "POST":
        patente = request.POST.get("patente", "").strip().upper()
        headers = _headers(request)
        if not headers:
            messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
            return redirect("login")
        try:
            resp = requests.get(f"{API_BASE}/estacionamientos/", headers=headers)
            if resp.status_code == 200:
                est = next((e for e in resp.json() if e.get("patente") == patente and e.get("estado") == "O"), None)
                if est:
                    requests.post(f"{API_BASE}/estacionamientos/{est['id']}/liberar/", headers=headers)
                    messages.success(request, "Salida registrada.")
                else:
                    messages.error(request, "No se encontró estacionamiento ocupado con esa patente")
        except requests.RequestException as e:
            messages.error(request, f"Error de conexión con la API: {e}")
    return redirect("home")
