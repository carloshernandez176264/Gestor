from django.db import models
from Gestor_tareas.models.cliente import Cliente


class Empleado(models.Model):
    # Información básica
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", null=True, blank=True)
    direccion = models.TextField(verbose_name="Dirección", null=True, blank=True)

    # Información laboral
    puesto = models.CharField(max_length=100, verbose_name="Puesto")
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario")
    fecha_contratacion = models.DateField(verbose_name="Fecha de Contratación")
    fecha_termino = models.DateField(verbose_name="Fecha de Término", null=True, blank=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='empleados',
        verbose_name="Cliente Asociado"
    )

    # Información adicional
    activo = models.BooleanField(default=True, verbose_name="¿Empleado Activo?")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    numero_identificacion = models.CharField(max_length=50, unique=True, verbose_name="Número de Identificación")
    notas = models.TextField(verbose_name="Notas", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.puesto}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['nombre']
