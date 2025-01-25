from django.urls import path
from Gestor_tareas.views.informe_views import generar_informe, exportar_informe

urlpatterns = [
    path('informes/', generar_informe, name='generar_informe'),
    path('informes/exportar/', exportar_informe, name='exportar_informe'),
]
