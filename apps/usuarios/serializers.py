from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Usuario
from .forms.usuarios import UsuarioForm, RegistroClienteForm

class UsuarioSerializer(serializers.ModelSerializer):
    clave = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'numeroTelefono', 'rol', 'discapacidad', 'clave']
        read_only_fields = ('created_at',)

    def validate(self, datos):
        datosValidacion = datos.copy()
        if 'clave' in datosValidacion:
            datosValidacion['confirmar_clave'] = datosValidacion['clave']
            
        formulario = UsuarioForm(data=datosValidacion, instance=self.instance)
        if not formulario.is_valid():
            raise serializers.ValidationError(formulario.errors)
        return datos

    def create(self, datosValidados):
        clave = datosValidados.pop("clave", "temporal")
        usuario = Usuario(**datosValidados)
        usuario.setClave(clave)
        usuario.save()
        try:
            User.objects.create_user(
                username=str(usuario.rut),
                password=clave
            )
        except Exception:
            pass
        return usuario

    def update(self, instancia, datosValidados):
        clave = datosValidados.pop('clave', None)
        
        for campo, valor in datosValidados.items():
            setattr(instancia, campo, valor)
        
        if clave:
            instancia.setClave(clave)
        
        instancia.save()
        return instancia

class RegistroClienteSerializer(serializers.ModelSerializer):
    clave = serializers.CharField(write_only=True, min_length=8)
    confirmarClave = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 
                 'numeroTelefono', 'clave', 'confirmarClave', 'discapacidad']

    def validate(self, datos):
        if datos['clave'] != datos['confirmarClave']:
            raise serializers.ValidationError({'clave': 'Las contraseñas no coinciden'})
        
        datosFormulario = datos.copy()
        datosFormulario.pop('confirmarClave')
        
        formulario = RegistroClienteForm(data=datosFormulario)
        if not formulario.is_valid():
            raise serializers.ValidationError(formulario.errors)
        
        return datos

    def create(self, datosValidados):
        clave = datosValidados.pop('clave')
        datosValidados.pop('confirmarClave')
        
        usuario = Usuario(**datosValidados)
        usuario.rol = 'Cliente'
        usuario.setClave(clave)
        usuario.save()
        
        try:
            User.objects.create_user(
                username=str(usuario.rut),
                password=clave
            )
        except Exception:
            pass
            
        return usuario

class UsuarioLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    clave = serializers.CharField()

    def validate(self, datos):
        username = datos['username']
        password = datos['clave']
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError('Usuario o contraseña incorrectos.')
        
        try:
            usuario = Usuario.objects.get(rut=int(username))
            datos['usuario'] = usuario
            datos['usuarioDjango'] = user
        except (Usuario.DoesNotExist, ValueError):
            raise serializers.ValidationError('Usuario no encontrado.')
        
        return datos


class UsuarioPublicoSerializer(serializers.ModelSerializer):
    nombreCompleto = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        exclude = ['clave']

    def get_nombreCompleto(self, objeto):
        return f"{objeto.nombre} {objeto.apellidoPaterno} {objeto.apellidoMaterno}"