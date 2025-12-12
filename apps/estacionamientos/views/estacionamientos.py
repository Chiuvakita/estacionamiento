from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from ..forms.estacionamientos import EstacionamientoForm, EstacionamientosMasivoForm
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado
from django.conf import settings

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
def listarEstacionamiento(request):
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")

    estacionamientos = []
    try:
        resp = requests.get(f"{API_BASE}/estacionamientos/", headers=headers)
        data = resp.json()
        if resp.status_code == 200:
            estacionamientos = data
        else:
            messages.error(request, "Error al cargar estacionamientos desde la API.")
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")

    return render(request, "estacionamiento/estacionamientoListar.html", {"estacionamientos": estacionamientos})

@loginRequerido
@soloAdminEmpleado
def crearEstacionamiento(request):
    if request.method == "POST":
        form = EstacionamientoForm(request.POST)
        if form.is_valid():
            headers = _headers(request)
            if not headers:
                messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
                return redirect("login")
            try:
                resp = requests.post(
                    f"{API_BASE}/estacionamientos/",
                    json=form.cleaned_data,
                    headers=headers,
                )
                if resp.status_code in (200, 201):
                    messages.success(request, "Estacionamiento creado.")
                    return redirect("listarEstacionamiento")
                else:
                    errors = resp.json().get("errors") or resp.json()
                    messages.error(request, f"Error al crear: {errors}")
            except requests.RequestException as e:
                messages.error(request, f"Error de conexión con la API: {e}")
    else:
        form = EstacionamientoForm()
    return render(request, "estacionamiento/estacionamientoCrear.html", {"form": form})

@loginRequerido
@soloAdminEmpleado
def crearEstacionamientosMasivo(request):
    if request.method == "POST":
        form = EstacionamientosMasivoForm(request.POST)
        if form.is_valid():
            headers = _headers(request)
            if not headers:
                messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
                return redirect("login")
            cantidad = form.cleaned_data["cantidad"]
            tipo = form.cleaned_data["tipo"]
            try:
                resp = requests.post(
                    f"{API_BASE}/estacionamientos/bulk/",
                    json={"cantidad": cantidad, "tipo": tipo},
                    headers=headers,
                )
                if resp.status_code in (200, 201):
                    messages.success(request, "Estacionamientos creados.")
                    return redirect("listarEstacionamiento")
                errors = resp.json()
                messages.error(request, f"Error al crear: {errors}")
            except requests.RequestException as e:
                messages.error(request, f"Error de conexión con la API: {e}")
    else:
        form = EstacionamientosMasivoForm()
    return render(request, "estacionamiento/estacionamientoCrearMasivo.html", {"form": form})

@loginRequerido
@soloAdminEmpleado
def editarEstacionamiento(request, id):
    headers = _headers(request)
    if not headers:
        messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
        return redirect("login")

    est_data = None
    try:
        resp = requests.get(f"{API_BASE}/estacionamientos/{id}/", headers=headers)
        if resp.status_code == 404:
            messages.error(request, "Estacionamiento no encontrado.")
            return redirect("listarEstacionamiento")
        est_data = resp.json()
    except requests.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {e}")
        return redirect("listarEstacionamiento")
    if request.method == "POST":
        form = EstacionamientoForm(request.POST)
        if form.is_valid():
            try:
                resp = requests.put(
                    f"{API_BASE}/estacionamientos/{id}/",
                    json=form.cleaned_data,
                    headers=headers,
                )
                if resp.status_code in (200, 202, 204):
                    messages.success(request, "Estacionamiento actualizado.")
                    return redirect("listarEstacionamiento")
                errors = resp.json().get("errors") or resp.json()
                messages.error(request, f"Error al actualizar: {errors}")
            except requests.RequestException as e:
                messages.error(request, f"Error de conexión con la API: {e}")
    else:
        initial = {
            "estado": est_data.get("estado"),
            "tipo": est_data.get("tipo"),
            "patente": est_data.get("patente"),
        }
        form = EstacionamientoForm(initial=initial)
    return render(request, "estacionamiento/estacionamientoEditar.html", {"form": form, "id": id})

@loginRequerido
@soloAdminEmpleado
def eliminarTodosEstacionamientos(request):
    if request.method == "POST":
        headers = _headers(request)
        if not headers:
            messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
            return redirect("login")
        try:
            resp = requests.delete(f"{API_BASE}/estacionamientos/purge/", headers=headers)
            if resp.status_code in (200, 204):
                messages.success(request, "Estacionamientos eliminados.")
            else:
                messages.error(request, f"Error al eliminar: {resp.json()}")
        except requests.RequestException as e:
            messages.error(request, f"Error de conexión con la API: {e}")
    return redirect("listarEstacionamiento")


@loginRequerido
@soloAdminEmpleado
def eliminarEstacionamiento(request, id):
    if request.method == "POST":
        headers = _headers(request)
        if not headers:
            messages.error(request, "Token no encontrado. Inicia sesión nuevamente.")
            return redirect("login")
        try:
            requests.delete(f"{API_BASE}/estacionamientos/{id}/", headers=headers)
            messages.success(request, "Estacionamiento eliminado.")
        except requests.RequestException as e:
            messages.error(request, f"Error de conexión con la API: {e}")
    return redirect("listarEstacionamiento")
