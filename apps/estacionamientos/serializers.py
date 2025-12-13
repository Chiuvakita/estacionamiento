from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers

from .models.estacionamiento import Estacionamiento
from .models.reserva import Reserva
from .models.historial import Historial
from .views.services import existe_reserva_activa_o_programada, ocupar_estacionamiento


class EstacionamientoSerializer(serializers.ModelSerializer):
    """Serializer para espacios de estacionamiento."""
    fechaInicio = serializers.DateTimeField(
        source="fecha_inicio", 
        allow_null=True, 
        required=False,
        help_text="Fecha y hora de inicio de ocupación (formato ISO 8601)"
    )
    fechaTermino = serializers.DateTimeField(
        source="fecha_termino", 
        allow_null=True, 
        required=False,
        help_text="Fecha y hora de liberación (formato ISO 8601)"
    )

    class Meta:
        model = Estacionamiento
        fields = ["id", "estado", "tipo", "patente", "fechaInicio", "fechaTermino"]


class ReservaSerializer(serializers.ModelSerializer):
    """Serializer para reservas de estacionamientos."""
    fechaInicio = serializers.DateTimeField(
        source="fecha_inicio",
        help_text="Fecha y hora de inicio de la reserva (formato ISO 8601). Debe ser al menos 2 horas en el futuro."
    )
    fechaTermino = serializers.DateTimeField(
        source="fecha_termino", 
        allow_null=True, 
        required=False,
        help_text="Fecha y hora de fin de la reserva (se calcula automáticamente)"
    )
    tipoSnapshot = serializers.CharField(
        source="tipo_snapshot", 
        read_only=True,
        help_text="Tipo de estacionamiento al momento de la reserva"
    )
    duracionHoras = serializers.IntegerField(
        write_only=True,
        help_text="Duración de la reserva en horas (mínimo 1 hora)"
    )
    tiempoRestante = serializers.SerializerMethodField(
        help_text="Tiempo restante de la reserva en formato legible (ej: '2h 30m')"
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "estacionamiento",
            "vehiculo",
            "fechaInicio",
            "fechaTermino",
            "tipoSnapshot",
            "duracionHoras",
            "tiempoRestante",
        ]

    def get_tiempoRestante(self, obj):
        return obj.tiempo_restante

    def validate(self, datos):
        duracion = datos.get("duracionHoras")
        if duracion is None or duracion <= 0:
            raise serializers.ValidationError({"duracionHoras": "Duracion: min 1 hora"})
        est = datos.get("estacionamiento")
        if est and est.estado != "D":
            raise serializers.ValidationError({"estacionamiento": "Estacionamiento no disponible"})
        if existe_reserva_activa_o_programada():
            raise serializers.ValidationError({"non_field_errors": ["Reserva activa existe"]})
        return datos

    def create(self, datos):
        fecha_inicio = datos.get("fecha_inicio", timezone.now())
        duracion = datos.get("duracionHoras")
        fecha_termino = fecha_inicio + timedelta(hours=duracion)
        datos["fecha_termino"] = fecha_termino
        datos["tipo_snapshot"] = datos["estacionamiento"].tipo

        reserva = Reserva.objects.create(
            estacionamiento=datos["estacionamiento"],
            vehiculo=datos["vehiculo"],
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
            tipo_snapshot=datos["tipo_snapshot"],
        )

        ocupar_estacionamiento(
            est=datos["estacionamiento"],
            patente=datos["vehiculo"].patente,
            fecha_inicio=fecha_inicio,
            es_reserva=True,
        )
        return reserva


class HistorialSerializer(serializers.ModelSerializer):
    fechaInicio = serializers.DateTimeField(source="fecha_inicio")
    fechaTermino = serializers.DateTimeField(source="fecha_termino", allow_null=True, required=False)

    class Meta:
        model = Historial
        fields = ["id", "estacionamiento", "vehiculo", "fechaInicio", "fechaTermino", "es_reserva"]
