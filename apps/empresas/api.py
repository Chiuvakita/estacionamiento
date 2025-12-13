from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.empresas.models import Empresa, Sucursal
from apps.empresas.serializers import EmpresaSerializer, SucursalSerializer, SucursalListSerializer
from apps.usuarios.models import Usuario


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    API para gestión de empresas del sistema.
    
    CRUD completo disponible para Admin/Empleado:
    - list: Lista todas las empresas registradas
    - create: Registra una nueva empresa
    - retrieve: Obtiene detalles de una empresa
    - update/partial_update: Modifica datos de empresa
    - destroy: Elimina una empresa
    
    Acción adicional:
    - sucursales: Lista todas las sucursales de una empresa específica
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    
    def _usuario(self, solicitud):
        nombreUsuario = getattr(solicitud.user, "username", "")
        if str(nombreUsuario).isdigit():
            return Usuario.objects.filter(rut=int(nombreUsuario)).first()
        return None
    
    def list(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        empresas = self.get_queryset()
        serializador = self.get_serializer(empresas, many=True)
        return Response(serializador.data)
    
    def create(self, solicitud):
        serializador = self.get_serializer(data=solicitud.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            empresa = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(empresa)
            return Response(serializador.data)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            empresa = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(empresa, data=solicitud.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def partial_update(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            empresa = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(empresa, data=solicitud.data, partial=True)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            empresa = self.get_queryset().get(pk=pk)
            empresa.delete()
            return Response(
                {"mensaje": "Empresa eliminada correctamente"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def sucursales(self, solicitud, pk=None):
        """
        Lista todas las sucursales asociadas a una empresa.
        
        Retorna información completa de cada sucursal incluyendo:
        - Nombre de la sucursal
        - Dirección y número
        - Cantidad de estacionamientos
        """
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            empresa = self.get_queryset().get(pk=pk)
            sucursales = Sucursal.objects.filter(empresa=empresa)
            serializador = SucursalListSerializer(sucursales, many=True)
            return Response(serializador.data)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class SucursalViewSet(viewsets.ModelViewSet):
    """
    API para gestión de sucursales de empresas.
    
    CRUD completo para Admin/Empleado:
    - list: Lista sucursales (filtrable por empresa con query param empresa_id)
    - create: Crea una nueva sucursal asociada a una empresa
    - retrieve: Obtiene detalles de una sucursal
    - update/partial_update: Modifica datos de sucursal
    - destroy: Elimina una sucursal
    """
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated]
    
    def _usuario(self, solicitud):
        nombreUsuario = getattr(solicitud.user, "username", "")
        if str(nombreUsuario).isdigit():
            return Usuario.objects.filter(rut=int(nombreUsuario)).first()
        return None
    
    def get_queryset(self):
        consulta = Sucursal.objects.all()
        empresaId = self.request.query_params.get('empresa_id', None)
        if empresaId is not None:
            consulta = consulta.filter(empresa_id=empresaId)
        return consulta
    
    def list(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        sucursales = self.get_queryset()
        serializador = SucursalListSerializer(sucursales, many=True)
        return Response(serializador.data)
    
    def create(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        serializador = self.get_serializer(data=solicitud.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            sucursal = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(sucursal)
            return Response(serializador.data)
        except Sucursal.DoesNotExist:
            return Response(
                {"error": "Sucursal no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            sucursal = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(sucursal, data=solicitud.data)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Sucursal.DoesNotExist:
            return Response(
                {"error": "Sucursal no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def partial_update(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            sucursal = self.get_queryset().get(pk=pk)
            serializador = self.get_serializer(sucursal, data=solicitud.data, partial=True)
            if serializador.is_valid():
                serializador.save()
                return Response(serializador.data)
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
        except Sucursal.DoesNotExist:
            return Response(
                {"error": "Sucursal no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            sucursal = self.get_queryset().get(pk=pk)
            sucursal.delete()
            return Response(
                {"mensaje": "Sucursal eliminada correctamente"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Sucursal.DoesNotExist:
            return Response(
                {"error": "Sucursal no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
