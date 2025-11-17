from django.contrib import admin
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("id", "patente", "marca", "modelo", "tipo")
    search_fields = ("patente", "marca", "modelo")
    ordering = ("patente",)
