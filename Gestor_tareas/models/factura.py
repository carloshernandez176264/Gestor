from django.db import models
from Gestor_tareas.models import Cliente, Empleado

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=20, unique=True)  # Nuevo campo
    fecha_emision = models.DateField()  # Nuevo campo
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre}"