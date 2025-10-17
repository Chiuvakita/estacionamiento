from django.shortcuts import render
from ..models.historial import Historial

def listarHistorial(request):
    historial = Historial.objects.all().order_by("estacionamiento_id", "-fecha_inicio")

    total_registros = historial.count()
    total_reservas = historial.filter(es_reserva=True).count()
    total_estacionamientos = historial.values("estacionamiento_id").distinct().count()

    return render(request, "historial/historialListar.html", {
        "historial": historial,
        "total_reservas": total_reservas,
        "total_registros": total_registros,
        "total_estacionamientos": total_estacionamientos
    })
