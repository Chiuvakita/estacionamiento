from django.shortcuts import render, redirect
from datetime import datetime, timedelta

# ===========================
# Simulación de base de datos
# ===========================
estacionamientos = []
reservas = []    
historial = []    


# ===========================
# HOME (principal)
# ===========================
def home(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        modo = request.POST.get("modo")

        if modo == "especifico":
            estId = int(request.POST.get("estacionamiento_id"))
            estacionamiento = next((e for e in estacionamientos if e["id"] == estId and e["estado"] == "Disponible"), None)
        else:
            estacionamiento = next((e for e in estacionamientos if e["estado"] == "Disponible"), None)

        if estacionamiento:
            estacionamiento["estado"] = "Ocupado"
            estacionamiento["patente"] = patente
            estacionamiento["fechaInicio"] = datetime.now()
            estacionamiento["fechaTermino"] = None

            # Guardamos en historial (NO en reservas)
            movimiento = {
                "id": len(historial) + 1,
                "estacionamiento_id": estacionamiento["id"],
                "patente": patente,
                "fechaInicio": datetime.now(),
                "fechaTermino": None,
                "tipo": estacionamiento["tipo"],
                "reserva": False
            }
            historial.append(movimiento)

        return redirect("home")

    disponibles = sum(1 for e in estacionamientos if e["estado"] == "Disponible")
    ocupados = [e for e in estacionamientos if e["estado"] == "Ocupado"]

    return render(request, "main/home.html", {
        "disponibles": disponibles,
        "ocupados": ocupados,
        "estacionamientos": estacionamientos
    })


def marcarSalida(request, id):
    estacionamiento = next((e for e in estacionamientos if e["id"] == id), None)
    if estacionamiento:
        estacionamiento["estado"] = "Disponible"
        estacionamiento["patente"] = None
        estacionamiento["fechaTermino"] = datetime.now()

        # Buscar en historial
        mov = next((r for r in historial if r["estacionamiento_id"] == id and r["fechaTermino"] is None), None)
        if mov:
            mov["fechaTermino"] = datetime.now()

    return redirect("home")


def marcarSalidaPatente(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        estacionamiento = next((e for e in estacionamientos if e["patente"] == patente), None)
        if estacionamiento:
            estacionamiento["estado"] = "Disponible"
            estacionamiento["patente"] = None
            estacionamiento["fechaTermino"] = datetime.now()

            mov = next((r for r in historial if r["patente"] == patente and r["fechaTermino"] is None), None)
            if mov:
                mov["fechaTermino"] = datetime.now()

    return redirect("home")



# ===========================
# ESTACIONAMIENTOS (admin)
# ===========================
def listarEstacionamiento(request):
    return render(request, "estacionamiento/estacionamientoListar.html", {"estacionamientos": estacionamientos})


def crearEstacionamiento(request):
    if request.method == "POST":
        nuevo = {
            "id": len(estacionamientos) + 1,
            "estado": request.POST.get("estado", "Disponible"),
            "tipo": request.POST.get("tipo", "Normal"),
        }
        estacionamientos.append(nuevo)
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoCrear.html")


def crearEstacionamientosMasivo(request):
    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad", 1))
        tipo = request.POST.get("tipo", "Normal")
        for _ in range(cantidad):
            nuevo = {
                "id": len(estacionamientos) + 1,
                "estado": "Disponible",
                "tipo": tipo,
                "patente": None,
                "fechaInicio": None,
                "fechaTermino": None,
            }
            estacionamientos.append(nuevo)
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoCrearMasivo.html")


def editarEstacionamiento(request, id):
    estacionamiento = next((e for e in estacionamientos if e["id"] == id), None)
    if request.method == "POST" and estacionamiento:
        estacionamiento["estado"] = request.POST.get("estado", estacionamiento["estado"])
        estacionamiento["tipo"] = request.POST.get("tipo", estacionamiento["tipo"])
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEditar.html", {"id": id, "estacionamiento": estacionamiento})


def eliminarEstacionamiento(request, id):
    global estacionamientos
    if request.method == "POST":
        estacionamientos = [e for e in estacionamientos if e["id"] != id]
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEliminar.html", {"id": id})


def eliminarTodosEstacionamientos(request):
    global estacionamientos, reservas
    if request.method == "POST":
        estacionamientos = []
        reservas = []
        return redirect("listarEstacionamiento")
    return render(request, "estacionamiento/estacionamientoEliminarTodos.html")


# ===========================
# RESERVAS (cliente)
# ===========================
def listarReserva(request):
    data = []
    ahora = datetime.now()

    for r in reservas:
        # duración total de la reserva
        duracion = (r["fechaTermino"] - r["fechaInicio"]).total_seconds() / 3600 if r["fechaTermino"] else 0
        duracion_str = f"{int(duracion)} horas" if duracion else "-"

        # calcular tiempo restante
        if r["fechaTermino"] and r["fechaTermino"] > ahora:
            diff = r["fechaTermino"] - ahora
            horas = diff.seconds // 3600
            minutos = (diff.seconds % 3600) // 60
            tiempo_restante = f"{horas}h {minutos}m"
        else:
            tiempo_restante = "Finalizada"

        data.append({
            "id": r["id"],
            "patente": r["patente"],
            "estacionamiento_id": r["estacionamiento_id"],
            "fechaInicio": r["fechaInicio"].strftime("%Y-%m-%d %H:%M"),
            "fechaTermino": r["fechaTermino"].strftime("%Y-%m-%d %H:%M") if r["fechaTermino"] else "-",
            "duracion": duracion_str,
            "tiempoRestante": tiempo_restante
        })

    return render(request, "reserva/reservaListar.html", {"reservas": data})



def crearReserva(request):
    if request.method == "POST":
        patente = request.POST.get("patente")
        fecha_inicio = datetime.strptime(request.POST.get("fechaInicio"), "%Y-%m-%dT%H:%M")
        duracion_horas = int(request.POST.get("duracion"))
        fecha_termino = fecha_inicio + timedelta(hours=duracion_horas)

        estId = int(request.POST.get("estacionamiento_id"))
        estacionamiento = next((e for e in estacionamientos if e["id"] == estId), None)

        if estacionamiento and estacionamiento["estado"] == "Disponible":
            reserva = {
                "id": len(reservas) + 1,
                "estacionamiento_id": estId,
                "patente": patente,
                "fechaInicio": fecha_inicio,
                "fechaTermino": fecha_termino,
                "tipo": estacionamiento["tipo"],
                "reserva": True
            }
            reservas.append(reserva)
            historial.append(reserva.copy())

            estacionamiento["estado"] = "Ocupado"
            estacionamiento["patente"] = patente

        return redirect("listarReserva")

    return render(request, "reserva/crearReserva.html", {"estacionamientos": estacionamientos})


def terminarReserva(request, id):
    reserva = next((r for r in reservas if r["id"] == id), None)
    if reserva:
        estacionamiento = next((e for e in estacionamientos if e["id"] == reserva["estacionamiento_id"]), None)
        if estacionamiento:
            estacionamiento["estado"] = "Disponible"
            estacionamiento["patente"] = None
        reserva["fechaTermino"] = datetime.now()
    return redirect("listarReserva")


# ===========================
# HISTORIAL
# ===========================
def listarHistorial(request):
    total_reservas = sum(1 for r in historial if r.get("reserva"))
    return render(request, "historial/historialListar.html", {
        "reservas": historial,
        "total_reservas": total_reservas
    })

