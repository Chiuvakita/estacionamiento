from rest_framework import serializers
from .models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'
    
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
