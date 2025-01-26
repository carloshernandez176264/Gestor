from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Gestor_tareas.models import Venta, Factura

@login_required
def listar_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/listar_ventas.html', {'ventas': ventas})

@login_required
def agregar_venta(request):
    if request.method == 'POST':
        factura_id = request.POST.get('factura_id')
        producto = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')

        factura = Factura.objects.get(id=factura_id)

        Venta.objects.create(
            factura=factura,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        return redirect('listar_ventas')
    return render(request, 'ventas/agregar_venta.html')

@login_required
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        venta.producto = request.POST.get('producto')
        venta.cantidad = request.POST.get('cantidad')
        venta.precio_unitario = request.POST.get('precio_unitario')
        venta.save()
        return redirect('listar_ventas')
    return render(request, 'ventas/editar_venta.html', {'venta': venta})

@login_required
def eliminar_venta(request, venta_id):
    venta = Venta.objects.get(id=venta_id)
    if request.method == 'POST':
        venta.delete()
        return redirect('listar_ventas')
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})
