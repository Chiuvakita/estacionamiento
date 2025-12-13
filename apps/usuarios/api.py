from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Usuario
from .serializers import UsuarioSerializer, RegistroClienteSerializer, UsuarioLoginSerializer, UsuarioPublicoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API para gestión completa de usuarios del sistema.
    
    Operaciones:
    - list: Retorna todos los usuarios (acceso público)
    - create: Crea un nuevo usuario (requiere rol Admin/Empleado)
    - retrieve: Obtiene un usuario específico por RUT
    - update: Actualiza datos de un usuario existente
    - partial_update: Actualización parcial de usuario
    - destroy: Elimina un usuario del sistema
    
    Acciones adicionales:
    - registro: Registro público para nuevos clientes
    - login: Autenticación y generación de token de acceso
    - logout: Cierra sesión y elimina el token del usuario
    """
    queryset = Usuario.objects.all()
    lookup_field = 'rut'
    
    def get_serializer_class(self):
        if self.action == 'registro':
            return RegistroClienteSerializer
        elif self.action == 'login':
            return UsuarioLoginSerializer
        return UsuarioPublicoSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['registro', 'login', 'list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

    def create(self, request):
        if hasattr(request.user, 'username') and request.user.username.isdigit():
            try:
                usuarioAutenticado = Usuario.objects.get(rut=int(request.user.username))
                if usuarioAutenticado.rol not in ['Administrador', 'Empleado']:
                    return Response({
                        'success': False,
                        'errors': {'non_field_errors': ['No tienes permisos para crear usuarios']}
                    }, status=403)
            except Usuario.DoesNotExist:
                return Response({
                    'success': False,
                    'errors': {'non_field_errors': ['Usuario no encontrado']}
                }, status=403)
        else:
            return Response({
                'success': False,
                'errors': {'non_field_errors': ['Acceso denegado']}
            }, status=403)
        
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'success': True,
                'usuario': UsuarioPublicoSerializer(usuario).data
            }, status=201)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=400)

    def update(self, request, rut=None):
        try:
            usuario = Usuario.objects.get(rut=rut)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
            
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'success': True,
                'usuario': UsuarioPublicoSerializer(usuario).data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=400)

    def list(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioPublicoSerializer(usuarios, many=True)
        return Response({
            'success': True,
            'usuarios': serializer.data
        })

    def destroy(self, request, rut=None):
        try:
            usuario = Usuario.objects.get(rut=rut)
            usuario.delete()
            return Response({
                'success': True,
                'message': 'Usuario eliminado'
            })
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

    @action(detail=False, methods=['post'])
    def registro(self, request):
        """
        Registra un nuevo cliente en el sistema.
        
        Parámetros requeridos:
        - rut: RUT del cliente (número entero)
        - nombre, apellidoPaterno, apellidoMaterno: Datos personales
        - numeroTelefono: Teléfono de contacto
        - clave: Contraseña (mínimo 8 caracteres)
        - confirmarClave: Confirmación de contraseña (debe coincidir)
        - discapacidad: Booleano indicando si tiene discapacidad
        
        Retorna el usuario creado y asigna automáticamente el rol 'Cliente'.
        """
        serializer = RegistroClienteSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'success': True,
                'usuario': UsuarioPublicoSerializer(usuario).data
            }, status=201)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=400)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Autentica un usuario y genera un token de acceso.
        
        Parámetros:
        - username: RUT del usuario
        - clave: Contraseña del usuario
        
        Retorna:
        - token: Token de autenticación para usar en headers (Authorization: Token <token>)
        - usuario: Datos públicos del usuario autenticado
        """
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            user = serializer.validated_data['usuarioDjango']
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'token': token.key,
                'usuario': UsuarioPublicoSerializer(usuario).data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=400)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        return Response({'success': True, 'message': 'Logout exitoso'})