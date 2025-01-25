"""
URL configuration for Gestor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin
    path('clientes/', include('Gestor_tareas.urls.cliente_urls')),  # URLs de clientes
    path('empleados/', include('Gestor_tareas.urls.empleado_urls')),  # URLs de empleados
    path('ventas/', include('Gestor_tareas.urls.venta_urls')),  # URLs de ventas
    path('facturas/', include('Gestor_tareas.urls.factura_urls')),  # URLs de facturas
    path('informes/', include('Gestor_tareas.urls.informe_urls')),  # URLs de informes
]

