from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Tarea
from datetime import datetime
from django.utils.timezone import make_aware 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django import forms
from django.contrib.auth.models import User
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.html import format_html
from django.core.mail import EmailMultiAlternatives

# Create your views here.
@login_required
def lista_tareas(request):
    tareas = Tarea.objects.filter(usuario=request.user)  # Filtrar por usuario
    return render(request, 'tareas/lista_tareas.html', {'tareas': tareas} )

@login_required
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
            fecha_vencimiento = fecha_vencimiento,
            usuario=request.user  # Aseguramos que la tarea se asocie al usuario
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

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)  # Usar el formulario personalizado
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.email = form.cleaned_data.get('email', 'usuario@default.com')  # Captura el email o usa el predeterminado
            usuario.save()
            login(request, usuario)  # Autenticar al usuario después del registro
            return redirect('lista_tareas')  # Redirigir a la lista de tareas
    else:
        form = RegistroForm()

    return render(request, "tareas/usuarios_registro.html", {"form": form})


def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige al login después de cerrar sesión

def tareas_proximas_vencer():
    """Devuelve un diccionario con los usuarios y sus tareas próximas a vencer"""
    limite = now() + timedelta(days=1)  # Tareas que vencen en las próximas 24 horas
    tareas = Tarea.objects.filter(fecha_vencimiento__lte=limite, completada=False)
    
    usuarios_tareas = {}
    for tarea in tareas:
        if tarea.usuario not in usuarios_tareas:
            usuarios_tareas[tarea.usuario] = []
        usuarios_tareas[tarea.usuario].append(tarea)
    
    return usuarios_tareas

def enviar_alertas_tareas():
    usuarios_tareas = tareas_proximas_vencer()
    for usuario, tareas in usuarios_tareas.items():
        asunto = "🔔 Recordatorio: Tareas Próximas a Vencer"

        # Crear la estructura HTML del correo
        mensaje_html = f"""
        <html>
        <body>
            <h2 style="color: #2c3e50;">🔔 Recordatorio de Tareas Pendientes</h2>
            <p>Hola <b>{usuario.username}</b>, estas son tus tareas próximas a vencer:</p>
            <ul style="list-style-type: square; color: #2980b9;">
        """

        for tarea in tareas:
            mensaje_html += f"<li><b>{tarea.titulo}</b> - vence el {tarea.fecha_vencimiento.strftime('%d/%m/%Y %H:%M')}</li>"

        mensaje_html += """
            </ul>
            <p style="color: #e74c3c;">⏳ No dejes que el tiempo se acabe.</p>
            <br>
            <p>📌 <a href="https://sgt-c8if.onrender.com/tareas/">Accede a tu lista de tareas</a></p>
        </body>
        </html>
        """

        # Enviar correo en formato HTML
        mensaje = EmailMultiAlternatives(
            asunto,
            format_html(mensaje_html),  # HTML del mensaje
            'moralcorpprojects@gmail.com',  # Remitente
            [usuario.email]  # Destinatario
        )
        mensaje.attach_alternative(mensaje_html, "text/html")  # Adjuntar versión HTML
        mensaje.send()

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(enviar_alertas_tareas, 'interval', hours=24, next_run_time=now() + timedelta(seconds=10))
    scheduler.start()