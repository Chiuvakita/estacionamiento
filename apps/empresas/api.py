from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.empresas.models import Empresa, Sucursal
from apps.empresas.serializers import EmpresaSerializer, SucursalSerializer, SucursalListSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, solicitud):
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
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        consulta = Sucursal.objects.all()
        empresaId = self.request.query_params.get('empresa_id', None)
        if empresaId is not None:
            consulta = consulta.filter(empresa_id=empresaId)
        return consulta
    
    def list(self, solicitud):
        sucursales = self.get_queryset()
        serializador = SucursalListSerializer(sucursales, many=True)
        return Response(serializador.data)
    
    def create(self, solicitud):
        serializador = self.get_serializer(data=solicitud.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, solicitud, pk=None):
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
