from django.urls import path
from Gestor_tareas.views.factura_views import agregar_factura, editar_factura, eliminar_factura, listar_facturas

urlpatterns = [
    path('agregar/', agregar_factura, name='agregar_factura'),
    path('editar/<int:factura_id>/', editar_factura, name='editar_factura'),
    path('eliminar/<int:factura_id>/', eliminar_factura, name='eliminar_factura'),
    path('', listar_facturas, name='listar_facturas'),
]
