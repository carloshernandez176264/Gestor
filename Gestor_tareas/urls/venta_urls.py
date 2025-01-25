from django.urls import path
from Gestor_tareas.views.venta_views import listar_ventas, agregar_venta, editar_venta, eliminar_venta

urlpatterns = [
    path('ventas/', listar_ventas, name='listar_ventas'),
    path('ventas/agregar/', agregar_venta, name='agregar_venta'),
    path('ventas/editar/<int:venta_id>/', editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:venta_id>/', eliminar_venta, name='eliminar_venta'),
]
