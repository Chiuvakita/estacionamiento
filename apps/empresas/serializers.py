from rest_framework import serializers
from apps.empresas.models import Empresa, Sucursal


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para empresas del sistema."""
    class Meta:
        model = Empresa
        fields = '__all__'
        extra_kwargs = {
            'nombre': {'help_text': 'Nombre de la empresa (máximo 300 caracteres)'},
            'telefono': {'help_text': 'Teléfono de contacto de la empresa'},
            'correo': {'help_text': 'Correo electrónico corporativo'},
            'direccion': {'help_text': 'Dirección principal de la empresa'}
        }
    
    def validateNombre(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Nombre requerido")
        if len(valor) > 300:
            raise serializers.ValidationError("Nombre: max 300 caracteres")
        return valor.strip()
    
    def validateTelefono(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Telefono requerido")
        if not valor.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Telefono: solo numeros")
        return valor.strip()
    
    def validateCorreo(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Correo requerido")
        return valor.strip().lower()


class SucursalSerializer(serializers.ModelSerializer):
    """Serializer completo para sucursales de empresas."""
    empresaNombre = serializers.CharField(
        source='empresa.nombre', 
        read_only=True,
        help_text="Nombre de la empresa a la que pertenece la sucursal"
    )
    
    class Meta:
        model = Sucursal
        fields = '__all__'
        extra_kwargs = {
            'empresa': {'help_text': 'ID de la empresa a la que pertenece esta sucursal'},
            'nombreSucursal': {'help_text': 'Nombre de la sucursal (máximo 100 caracteres)'},
            'direccion': {'help_text': 'Dirección de la sucursal'},
            'numero': {'help_text': 'Número de la dirección'},
            'cantidadEstacionamiento': {'help_text': 'Cantidad total de espacios de estacionamiento (1-1000)'}
        }
    
    def validateNombreSucursal(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Nombre sucursal requerido")
        if len(valor) > 100:
            raise serializers.ValidationError("Nombre sucursal: max 100 caracteres")
        return valor.strip()
    
    def validateCantidadEstacionamiento(self, valor):
        if valor is None:
            raise serializers.ValidationError("Cantidad requerida")
        if valor < 1:
            raise serializers.ValidationError("Cantidad: min 1")
        if valor > 1000:
            raise serializers.ValidationError("Cantidad: max 1000")
        return valor
    
    def validateNumero(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Numero requerido")
        return valor.strip()
    
    def validateDireccion(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise serializers.ValidationError("Direccion requerida")
        return valor.strip()


class SucursalListSerializer(serializers.ModelSerializer):
    empresaNombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Sucursal
        fields = ['id', 'nombreSucursal', 'direccion', 'numero', 'cantidadEstacionamiento', 'empresa', 'empresaNombre']
