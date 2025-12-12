from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Usuario
from .serializers import UsuarioSerializer, RegistroClienteSerializer, UsuarioLoginSerializer, UsuarioPublicoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
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