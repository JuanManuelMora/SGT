from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Tarea
from datetime import datetime
from django.utils.timezone import make_aware 

# Create your views here.
def lista_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas/lista_tareas.html', {'tareas': tareas} )

def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        # Validación: La fecha de vencimiento no puede ser nula ni menor a la fecha actual
        if not fecha_vencimiento:
            return render(request, 'tareas/crear_tarea.html', {'error': 'Debes seleccionar una fecha de vencimiento'})
        
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%dT%H:%M")

        fecha_vencimiento = make_aware(fecha_vencimiento)

        if fecha_vencimiento < now():
            return render(request, 'tareas/crear_tarea.html', {'error': 'La fecha de vencimiento no puede ser anterior a la fecha actual.'})

        Tarea.objects.create(
            titulo = titulo,
            descripcion = descripcion,
            fecha_vencimiento = fecha_vencimiento
        )
        return redirect('lista_tareas')
    return render(request, 'tareas/crear_tarea.html')

def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id = id)
    if request.method == 'POST':
        tarea.titulo = request.POST.get('titulo')
        tarea.descripcion = request.POST.get('descripcion')
        tarea.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        tarea.save()
        return redirect('lista_tareas')
    return render(request, 'tareas/editar_tarea.html', {'tarea' : tarea})

def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id = id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    return render(request, 'tareas/eliminar_tarea.html', {'tarea' : tarea})

def completar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id = id)
    tarea.completada = True
    tarea.save()
    return redirect('lista_tareas')
