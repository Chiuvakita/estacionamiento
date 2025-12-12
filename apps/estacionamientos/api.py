from functools import wraps

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.usuarios.models import Usuario
from .models.estacionamiento import Estacionamiento
from .models.historial import Historial
from .models.reserva import Reserva
from .serializers import EstacionamientoSerializer, HistorialSerializer, ReservaSerializer
from .views.services import liberar_estacionamiento, ocupar_estacionamiento


class EstacionamientoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Estacionamiento.objects.all().order_by("id")
    serializer_class = EstacionamientoSerializer

    def _usuario(self, request):
        username = getattr(request.user, "username", "")
        if str(username).isdigit():
            return Usuario.objects.filter(rut=int(username)).first()
        return None

    def list(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["delete"], url_path="purge")
    def eliminar_todos(self, request):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        borrados, _ = Estacionamiento.objects.all().delete()
        return Response({"eliminados": borrados}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="ocupar")
    def ocupar(self, request, pk=None):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        patente = request.data.get("patente", "").strip().upper()
        if not patente:
            return Response({"patente": "Patente requerida"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            est = Estacionamiento.objects.get(pk=pk, estado="D")
        except Estacionamiento.DoesNotExist:
            return Response({"detail": "Estacionamiento no disponible"}, status=status.HTTP_400_BAD_REQUEST)
        ocupar_estacionamiento(est, patente)
        return Response(EstacionamientoSerializer(est).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="liberar")
    def liberar(self, request, pk=None):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        try:
            est = Estacionamiento.objects.get(pk=pk)
        except Estacionamiento.DoesNotExist:
            return Response({"detail": "Estacionamiento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        liberar_estacionamiento(est)
        return Response(EstacionamientoSerializer(est).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="bulk")
    def crear_masivo(self, request):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        cantidad = request.data.get("cantidad")
        tipo = request.data.get("tipo")
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return Response({"cantidad": "Debe ser un entero"}, status=status.HTTP_400_BAD_REQUEST)
        if cantidad <= 0:
            return Response({"cantidad": "Debe ser mayor a 0"}, status=status.HTTP_400_BAD_REQUEST)
        tipos_validos = [choice[0] for choice in Estacionamiento.TIPO_CHOICES]
        if tipo not in tipos_validos:
            return Response({"tipo": "Tipo inválido"}, status=status.HTTP_400_BAD_REQUEST)
        objs = [Estacionamiento(estado="D", tipo=tipo) for _ in range(cantidad)]
        creados = Estacionamiento.objects.bulk_create(objs)
        data = EstacionamientoSerializer(creados, many=True).data
        return Response(data, status=status.HTTP_201_CREATED)



class ReservaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reserva.objects.select_related("estacionamiento", "vehiculo").order_by("-id")
    serializer_class = ReservaSerializer

    def _usuario(self, request):
        username = getattr(request.user, "username", "")
        if str(username).isdigit():
            return Usuario.objects.filter(rut=int(username)).first()
        return None

    def list(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol != "Cliente":
            return Response({"detail": "Solo clientes pueden crear reservas"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def terminar(self, request, pk=None):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado", "Cliente"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        reserva = self.get_object()
        liberar_estacionamiento(reserva.estacionamiento)
        reserva.fecha_termino = timezone.now()
        reserva.save()
        serializer = self.get_serializer(reserva)
        return Response(serializer.data)



class HistorialViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Historial.objects.select_related("estacionamiento", "vehiculo").order_by("-fecha_inicio")
    serializer_class = HistorialSerializer

    def _usuario(self, request):
        username = getattr(request.user, "username", "")
        if str(username).isdigit():
            return Usuario.objects.filter(rut=int(username)).first()
        return None

    def list(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
