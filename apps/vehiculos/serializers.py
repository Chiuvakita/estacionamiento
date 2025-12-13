from rest_framework import serializers
from .models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    """Serializer para vehículos registrados en el sistema."""
    class Meta:
        model = Vehiculo
        fields = '__all__'
        extra_kwargs = {
            'patente': {'help_text': 'Patente del vehículo (6 caracteres alfanuméricos, ej: ABC123)'},
            'marca': {'help_text': 'Marca del vehículo (máximo 50 caracteres)'},
            'modelo': {'help_text': 'Modelo del vehículo (máximo 50 caracteres)'},
            'tipo': {'help_text': 'Tipo de vehículo (ej: Automóvil, Camioneta, Motocicleta)'}
        }
    
    def validatePatente(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Patente requerida")
        if len(valor) != 6:
            raise serializers.ValidationError("Patente: 6 caracteres")
        return valor.strip().upper()
    
    def validateMarca(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Marca requerida")
        if len(valor) > 50:
            raise serializers.ValidationError("Marca: max 50 caracteres")
        return valor.strip()
    
    def validateModelo(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Modelo requerido")
        if len(valor) > 50:
            raise serializers.ValidationError("Modelo: max 50 caracteres")
        return valor.strip()
    
    def validateTipo(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Tipo requerido")
        if len(valor) > 50:
            raise serializers.ValidationError("Tipo: max 50 caracteres")
        return valor.strip()
