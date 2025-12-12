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

    def _usuario(self, solicitud):
        nombreUsuario = getattr(solicitud.user, "username", "")
        if str(nombreUsuario).isdigit():
            return Usuario.objects.filter(rut=int(nombreUsuario)).first()
        return None

    def list(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(solicitud, *args, **kwargs)

    def retrieve(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(solicitud, *args, **kwargs)

    def create(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(solicitud, *args, **kwargs)

    def update(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(solicitud, *args, **kwargs)

    def destroy(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(solicitud, *args, **kwargs)

    @action(detail=False, methods=["delete"], url_path="purge")
    def eliminarTodos(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        borrados, _ = Estacionamiento.objects.all().delete()
        return Response({"eliminados": borrados}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="ocupar")
    def ocupar(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        patente = solicitud.data.get("patente", "").strip().upper()
        if not patente:
            return Response({"patente": "Patente requerida"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            estacionamiento = Estacionamiento.objects.get(pk=pk, estado="D")
        except Estacionamiento.DoesNotExist:
            return Response({"detail": "Estacionamiento no disponible"}, status=status.HTTP_400_BAD_REQUEST)
        ocupar_estacionamiento(estacionamiento, patente)
        return Response(EstacionamientoSerializer(estacionamiento).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="liberar")
    def liberar(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        try:
            estacionamiento = Estacionamiento.objects.get(pk=pk)
        except Estacionamiento.DoesNotExist:
            return Response({"detail": "Estacionamiento no existe"}, status=status.HTTP_404_NOT_FOUND)
        liberar_estacionamiento(estacionamiento)
        return Response(EstacionamientoSerializer(estacionamiento).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="bulk")
    def crearMasivo(self, solicitud):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        cantidad = solicitud.data.get("cantidad")
        tipo = solicitud.data.get("tipo")
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return Response({"cantidad": "Entero requerido"}, status=status.HTTP_400_BAD_REQUEST)
        if cantidad <= 0:
            return Response({"cantidad": "Cantidad: min 1"}, status=status.HTTP_400_BAD_REQUEST)
        tiposValidos = [opcion[0] for opcion in Estacionamiento.TIPO_CHOICES]
        if tipo not in tiposValidos:
            return Response({"tipo": "Tipo invalido"}, status=status.HTTP_400_BAD_REQUEST)
        objetos = [Estacionamiento(estado="D", tipo=tipo) for _ in range(cantidad)]
        creados = Estacionamiento.objects.bulk_create(objetos)
        datos = EstacionamientoSerializer(creados, many=True).data
        return Response(datos, status=status.HTTP_201_CREATED)



class ReservaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reserva.objects.select_related("estacionamiento", "vehiculo").order_by("-id")
    serializer_class = ReservaSerializer

    def _usuario(self, solicitud):
        nombreUsuario = getattr(solicitud.user, "username", "")
        if str(nombreUsuario).isdigit():
            return Usuario.objects.filter(rut=int(nombreUsuario)).first()
        return None

    def list(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(solicitud, *args, **kwargs)

    def retrieve(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(solicitud, *args, **kwargs)

    def create(self, solicitud, *args, **kwargs):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol != "Cliente":
            return Response({"detail": "Solo clientes"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(solicitud, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def terminar(self, solicitud, pk=None):
        usuario = self._usuario(solicitud)
        if not usuario or usuario.rol not in ["Administrador", "Empleado", "Cliente"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        reserva = self.get_object()
        liberar_estacionamiento(reserva.estacionamiento)
        reserva.fecha_termino = timezone.now()
        reserva.save()
        serializador = self.get_serializer(reserva)
        return Response(serializador.data)



class HistorialViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Historial.objects.select_related("estacionamiento", "vehiculo").order_by("-fecha_inicio")
    serializer_class = HistorialSerializer

    def _usuario(self, solicitud):
        nombreUsuario = getattr(solicitud.user, "username", "")
        if str(nombreUsuario).isdigit():
            return Usuario.objects.filter(rut=int(nombreUsuario)).first()
        return None

    def list(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        usuario = self._usuario(request)
        if not usuario or usuario.rol not in ["Administrador", "Empleado"]:
            return Response({"detail": "Sin autorizacion"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
