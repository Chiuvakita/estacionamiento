from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario
from .forms.usuarios import UsuarioForm, RegistroClienteForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpRequest
from .views import crearUsuarios, editarUsuario, registroView
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    clave = serializers.CharField(write_only=True, required=False)

    incluirDatosSensibles = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'numeroTelefono', 'rol', 'discapacidad', 'incluirDatosSensibles']
        read_only_fields = ('created_at')

    def validate(self, datos):
        formulario = UsuarioForm(data=datos, instance=self.instance)
        
        if not formulario.is_valid():
            raise serializers.ValidationError(formulario.errors)
        return datos

        
    def create(self, datosValidados):
        requestFalso = HttpRequest()
        requestFalso.method = 'POST'
        requestFalso.POST = datosValidados
        requestFalso.user = None 
        
        from django.contrib.auth.models import User
        try:
            usuarioAdmin = User.objects.filter(is_superuser=True).first()
            if usuarioAdmin:
                requestFalso.user = usuarioAdmin
        except:
            pass

    def update(self, instancia, datosValidados):
        requestFalso = HttpRequest()
        requestFalso.method = 'POST'
        requestFalso.POST = datosValidados
        requestFalso.user = None
        
        # Simular usuario admin
        try:
            usuarioAdmin = User.objects.filter(is_superuser=True).first()
            if usuarioAdmin:
                requestFalso.user = usuarioAdmin
        except:
            pass
        respuestaOriginal = editarUsuario(requestFalso, instancia.rut)
        
        usuarioActualizado = Usuario.objects.get(rut=instancia.rut)
        return usuarioActualizado


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
        requestFalso = HttpRequest()
        requestFalso.method = 'POST'
        requestFalso.POST = datosValidados
        
        respuestaOriginal = registroView(requestFalso)
        
        usuario = Usuario.objects.get(rut=datosValidados['rut'])
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