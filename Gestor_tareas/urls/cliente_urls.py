from django.urls import path
from Gestor_tareas.views.cliente_views import listar_clientes, agregar_cliente, editar_cliente, eliminar_cliente

urlpatterns = [
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('clientes/agregar/', agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
]
