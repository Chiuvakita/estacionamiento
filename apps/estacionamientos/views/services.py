from django.utils import timezone
from apps.estacionamientos.models.historial import Historial
from apps.estacionamientos.models.reserva import Reserva
from apps.vehiculos.models import Vehiculo

def ocupar_estacionamiento(est, patente, fecha_inicio=None, es_reserva=False):
    if fecha_inicio is None:
        fecha_inicio = timezone.now()

    # Simulación en Estacionamiento
    est.estado = "O"
    est.patente = patente
    est.fecha_inicio = fecha_inicio
    est.fecha_termino = None
    est.save()

    vehiculo = Vehiculo.objects.filter(patente=patente).first()

    Historial.objects.create(
        estacionamiento=est,
        vehiculo=vehiculo,
        fecha_inicio=fecha_inicio,
        fecha_termino=None,
        es_reserva=es_reserva
    )

def liberar_estacionamiento(est, fecha_termino=None):
    if fecha_termino is None:
        fecha_termino = timezone.now()

    est.estado = "D"
    est.patente = None
    est.fecha_termino = fecha_termino
    est.save()

    cerrar_historial_para(est, fecha_termino)

def cerrar_historial_para(est, fecha_termino):
    mov = (
        Historial.objects
        .filter(estacionamiento=est, fecha_termino__isnull=True)
        .order_by("-fecha_inicio")
        .first()
    )

    if mov:
        mov.fecha_termino = fecha_termino
        mov.save()

def existe_reserva_activa_o_programada(now=None):
    if now is None:
        now = timezone.now()

    return (
        Reserva.objects.filter(fecha_termino__isnull=True).exists()
        or Reserva.objects.filter(fecha_termino__gt=now).exists()
    )
