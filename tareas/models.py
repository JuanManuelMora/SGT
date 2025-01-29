from django.db import models
# importaciones para las validaciones de no crear tareas sin fecha de vencimiento ni tampoco permitir fechas de
# vencimiento posteriores a la fecha actual.
from django.core.exceptions import ValidationError
from django.utils.timezone import now

def validar_fecha_futura(value):
    if value < now():
        raise ValidationError('La fecha de vencimiento no puede ser anterior a la fecha actual.')

# Create your models here.
class Tarea(models.Model):
    titulo = models.CharField(max_length = 200, db_column='sgt_titulo')
    descripcion = models.TextField(db_column='sgt_descripcion')
    completada = models.BooleanField(default = False, db_column='sgt_completada')
    fecha_creacion = models.DateTimeField(auto_now_add = True, db_column='sgt_fechaCreacion')
    fecha_vencimiento = models.DateTimeField(null = True, blank = True, db_column='sgt_fechaVencimiento')

    class Meta:
        db_table = 'sgt'  # Usar minúsculas para evitar problemas con PostgreSQL

    def __str__(self):
        return self.titulo