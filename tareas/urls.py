from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tareas, name = 'lista_tareas'),
    path('crear/', views.crear_tarea, name = 'crear_tarea'),
    path('editar/<int:id>/', views.editar_tarea, name = 'editar_tarea'),
    path('eliminar/<int:id>/', views.eliminar_tarea, name = 'eliminar_tarea'),
    path('completar/<int:id>/', views.completar_tarea, name = 'completar_tarea'),
]