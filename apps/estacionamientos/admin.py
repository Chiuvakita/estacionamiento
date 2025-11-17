from django.contrib import admin
from .models.estacionamiento import Estacionamiento
from .models.reserva import Reserva
from .models.historial import Historial


# ======================================================
#   ADMIN — ESTACIONAMIENTOS (Crear 1 o muchos)
# ======================================================
@admin.register(Estacionamiento)
class EstacionamientoAdmin(admin.ModelAdmin):
    list_display = ("id", "estado", "tipo", "patente", "fecha_inicio", "fecha_termino")
    list_filter = ("estado", "tipo")

    readonly_fields = ("patente", "fecha_inicio", "fecha_termino")

    fields = ("estado", "tipo", "patente", "fecha_inicio", "fecha_termino")

    def has_change_permission(self, request, obj=None):
        if obj and obj.estado == "O":
            return False
        return True


# ======================================================
#   ADMIN — RESERVAS (Fecha de término SOLO lectura)
# ======================================================
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "vehiculo", "estacionamiento",
        "fecha_inicio", "fecha_termino", "tipo_snapshot"
    )
    list_filter = ("tipo_snapshot",)
    search_fields = ("vehiculo__patente",)

    readonly_fields = ("fecha_termino",)

    fields = ("vehiculo", "estacionamiento", "fecha_inicio", "fecha_termino", "tipo_snapshot")


# ======================================================
#   ADMIN — HISTORIAL (Solo lectura, no CRUD)
# ======================================================
@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = (
        "id", "vehiculo", "estacionamiento",
        "fecha_inicio", "fecha_termino", "es_reserva"
    )
    list_filter = ("es_reserva",)
    search_fields = ("vehiculo__patente",)
    ordering = ("-fecha_inicio",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
