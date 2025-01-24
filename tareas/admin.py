from django.contrib import admin
from .models import Tarea

# Register your models here.
@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'completada', 'fecha_creacion', 'fecha_vencimiento')
    list_filter = ('completada', 'fecha_creacion', 'fecha_vencimiento')
    search_fields = ('titulo', 'descripcion')
