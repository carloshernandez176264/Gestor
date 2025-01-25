from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=50)
    direccion = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
