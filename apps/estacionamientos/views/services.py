from django.utils import timezone
from ..models.estacionamiento import Estacionamiento
from ..models.reserva import Reserva
from ..models.historial import Historial

def ocupar_estacionamiento(est: Estacionamiento, patente: str, fecha_inicio=None, fecha_termino=None, es_reserva=False):
    if fecha_inicio is None:
        fecha_inicio = timezone.now()
    est.estado = "O"
    est.patente = patente
    est.fecha_inicio = fecha_inicio
    est.fecha_termino = fecha_termino
    est.save()

    Historial.objects.create(
        estacionamiento_id=est.id,
        patente=patente,
        fecha_inicio=fecha_inicio,
        fecha_termino=fecha_termino,
        es_reserva=es_reserva
    )

def liberar_estacionamiento(est: Estacionamiento, fecha_termino=None):
    if fecha_termino is None:
        fecha_termino = timezone.now()
    est.estado = "D"
    est.patente = None
    est.fecha_termino = fecha_termino
    est.save()
    cerrar_historial_para(est, fecha_termino)

def cerrar_historial_para(est: Estacionamiento, fecha_termino):
    mov = (
        Historial.objects
        .filter(estacionamiento_id=est.id, fecha_termino__isnull=True)
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
