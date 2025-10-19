from django.utils import timezone
from ..models.estacionamiento import Estacionamiento
from ..models.reserva import Reserva
from ..models.historial import Historial
from apps.utils.decoradores import loginRequerido, soloAdminEmpleado
@loginRequerido
@soloAdminEmpleado
def ocupar_estacionamiento(est: Estacionamiento, patente: str, fecha_inicio=None, fecha_termino=None, es_reserva=False):
    if fecha_inicio is None:
        fecha_inicio = timezone.now()
    est.estado = "O"
    est.patente = patente
    est.fecha_inicio = fecha_inicio
    est.fecha_termino = fecha_termino
    est.save()

    Historial.objects.create(
        estacionamiento=est,
        patente=patente,
        fecha_inicio=fecha_inicio,
        fecha_termino=fecha_termino,
        es_reserva=es_reserva
    )
@loginRequerido
@soloAdminEmpleado
def liberar_estacionamiento(est: Estacionamiento, fecha_termino=None):
    if fecha_termino is None:
        fecha_termino = timezone.now()
    est.estado = "D"
    est.patente = None
    est.fecha_termino = fecha_termino
    est.save()
    cerrar_historial_para(est, fecha_termino)
@loginRequerido
@soloAdminEmpleado
def cerrar_historial_para(est: Estacionamiento, fecha_termino):
    mov = Historial.objects.filter(estacionamiento=est, fecha_termino__isnull=True).last()
    if mov:
        mov.fecha_termino = fecha_termino
        mov.save()
@loginRequerido
@soloAdminEmpleado
def existe_reserva_activa_o_programada(now=None):
    if now is None:
        now = timezone.now()
    return Reserva.objects.filter(fecha_termino__isnull=True).exists() or \
           Reserva.objects.filter(fecha_termino__gt=now).exists()
