from django.shortcuts import render, redirect
from datetime import datetime

estacionamientos = [
    {"id": 1, "estado": "Disponible", "tipo": "Normal", "patente": None},
    {"id": 2, "estado": "Disponible", "tipo": "Discapacitado", "patente": None},
    {"id": 3, "estado": "Mantenimiento", "tipo": "VIP", "patente": None},
]

reservas = []


# Home
def home(request):
    return render(request, "home.html")

# Estacionamientos
# Realizar listarEstacionamiento
def listar_estacionamiento(request):
    return render(request, "estacionamiento/estacionamientoListar.html",{"estacionamientos":estacionamientos})



# Realizar crearEstacionamiento
def crear_estacionamiento(request):
    if request.method == "POST":
        nuevo = {
            "id": len(estacionamientos) + 1,
            "estado": request.POST.get("estado", "Disponible"),
            "tipo": request.POST.get("tipo", "Normal"),
            "patente": None
        }
        estacionamientos.append(nuevo)
        return redirect("estacionamientos_listar")
    return render(request, "estacionamiento/estacionamientoCrear.html")



# Realizar editarEstacionamiento
def editar_estacionamiento(request, id):
    return render(request, "estacionamiento/estacionamientoEditar.html", {"id": id})



# Realizar eliminarEstacionamiento
def eliminar_estacionamiento(request, id):
    return render(request, "estacionamiento/estacionamientoEliminar.html", {"id": id})


# ========================
# RESERVAS (Cliente)
# ========================
def listar_reserva(request):
    return render(request, "reserva/reservaListar.html", {"reservas": reservas})

def crear_reserva(request):
    if request.method == "POST":
        patente = request.POST.get("patente")

        # Revisar si ya existe una reserva activa para esa patente
        reserva_activa = next((r for r in reservas if r["patente"] == patente and r["fechaTermino"] is None), None)
        if reserva_activa:
            # Ya tiene una reserva activa → redirigimos sin crear
            return redirect("reservas_listar")

        est_id = int(request.POST.get("estacionamiento_id"))
        estacionamiento = next((e for e in estacionamientos if e["id"] == est_id), None)

        if estacionamiento and estacionamiento["estado"] == "Disponible":
            reserva = {
                "id": len(reservas) + 1,
                "estacionamiento_id": est_id,
                "patente": patente,
                "fechaInicio": datetime.now(),
                "fechaTermino": None,
            }
            reservas.append(reserva)
            estacionamiento["estado"] = "Ocupado"
            estacionamiento["patente"] = patente

        return redirect("reservas_listar")

    return render(request, "reserva/crearReserva.html", {"estacionamientos": estacionamientos})

def terminar_reserva(request, id):
    reserva = next((r for r in reservas if r["id"] == id), None)
    if reserva:
        estacionamiento = next((e for e in estacionamientos if e["id"] == reserva["estacionamiento_id"]), None)
        if estacionamiento:
            estacionamiento["estado"] = "Disponible"
            estacionamiento["patente"] = None
        reserva["fechaTermino"] = datetime.now()
    return redirect("reservas_listar")


# ========================
# MAIN (Administrador: ingreso directo)
# ========================
def main_ingreso(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        estacionamiento = next((e for e in estacionamientos if e["estado"] == "Disponible"), None)
        if estacionamiento:
            estacionamiento["estado"] = "Ocupado"
            estacionamiento["patente"] = patente
        return redirect("estacionamientos_listar")
    return render(request, "main/ingreso.html")