from django.shortcuts import render
from .models import Tarea

# Create your views here.
def lista_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas/lista_tareas.html', {'tareas': tareas} )