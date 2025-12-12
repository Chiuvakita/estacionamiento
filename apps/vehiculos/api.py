from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.vehiculos.models import Vehiculo
from apps.vehiculos.serializers import VehiculoSerializer
from apps.usuarios.models import Usuario


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all().order_by("patente")
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]
    
    def _usuario(self, solicitud):
        nombreUsuario = getattr(solicitud.user, "username", "")
        if str(nombreUsuario).isdigit():
            return Usuario.objects.filter(rut=int(nombreUsuario)).first()
        return None
    
    def list(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        vehiculos = self.get_queryset()
        serializador = self.get_serializer(vehiculos, many=True)
        return Response(serializador.data)
    
    def create(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        serializador = self.get_serializer(data=solicitud.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            vehiculo = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(vehiculo)
            return Response(serializador.data)
        except Vehiculo.DoesNotExist:
            return Response(
                {"error": "Vehiculo no existe"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            vehiculo = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(vehiculo, data=solicitud.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehiculo.DoesNotExist:
            return Response(
                {"error": "Vehiculo no existe"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def partial_update(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            vehiculo = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(vehiculo, data=solicitud.data, partial=True)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehiculo.DoesNotExist:
            return Response(
                {"error": "Vehiculo no existe"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            vehiculo = self.get_queryset().get(pk=pk)
            vehiculo.delete()
            return Response(
                {"mensaje": "Vehiculo eliminado correctamente"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Vehiculo.DoesNotExist:
            return Response(
                {"error": "Vehiculo no existe"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['delete'], url_path='purge')
    def eliminarTodos(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        borrados, _ = Vehiculo.objects.all().delete()
        return Response({"eliminados": borrados}, status=status.HTTP_200_OK)
