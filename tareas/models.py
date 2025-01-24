from django.db import models

# Create your models here.
class Tarea(models.Model):
    titulo = models.CharField(max_length = 200)
    descripcion = models.TextField()
    completada = models.BooleanField(default = False)
    fecha_creacion = models.DateTimeField(auto_now_add = True)
    fecha_vencimiento = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return self.titulo