from django.shortcuts import render
from ..models.historial import Historial
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado

@loginRequerido
@soloAdminEmpleado
def listarHistorial(request):
    historial = Historial.objects.all().order_by("estacionamiento_id", "-fecha_inicio")
    total_reservas = historial.filter(es_reserva=True).count()
    return render(request, "historial/historialListar.html", {
        "historial": historial,
        "total_reservas": total_reservas
    })
