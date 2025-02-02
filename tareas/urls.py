from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.urls import get_resolver
from django.http import HttpResponse
from .views import cerrar_sesion

def listar_urls(request):
    urls = [str(url.pattern) for url in get_resolver().url_patterns]
    return HttpResponse("<br>".join(urls))

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='tareas/login.html'), name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('', views.lista_tareas, name = 'lista_tareas'),
    path('crear/', views.crear_tarea, name = 'crear_tarea'),
    path('editar/<int:id>/', views.editar_tarea, name = 'editar_tarea'),
    path('eliminar/<int:id>/', views.eliminar_tarea, name = 'eliminar_tarea'),
    path('completar/<int:id>/', views.completar_tarea, name = 'completar_tarea'),
    path('show_urls/', listar_urls),  # Nueva ruta temporal para ver las URLs
]