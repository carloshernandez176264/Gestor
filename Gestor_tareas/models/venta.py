from django.db import models

from Gestor_tareas.models import Factura


class Venta(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='ventas')
    producto = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto} - {self.cantidad} unidades"
