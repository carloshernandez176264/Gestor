from django.urls import path
from Gestor_tareas.views.empleado_views import listar_empleados, agregar_empleado, editar_empleado, eliminar_empleado

urlpatterns = [
    path('empleados/', listar_empleados, name='listar_empleados'),
    path('empleados/agregar/', agregar_empleado, name='agregar_empleado'),
    path('empleados/editar/<int:empleado_id>/', editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', eliminar_empleado, name='eliminar_empleado'),
]
