from django.shortcuts import render, redirect, get_object_or_404
from Gestor_tareas.models import Empleado, Cliente


def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/listar_empleados.html', {'empleados': empleados})


def agregar_empleado(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        puesto = request.POST.get('puesto')
        salario = request.POST.get('salario')
        fecha_contratacion = request.POST.get('fecha_contratacion')
        cliente_id = request.POST.get('cliente_id')

        cliente = Cliente.objects.get(id=cliente_id)
        Empleado.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            puesto=puesto,
            salario=salario,
            fecha_contratacion=fecha_contratacion,
            cliente=cliente
        )
        return redirect('listar_empleados')

    return render(request, 'empleados/agregar_empleado.html', {'clientes': clientes})

def editar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.puesto = request.POST.get('puesto')
        empleado.salario = request.POST.get('salario')
        empleado.fecha_contratacion = request.POST.get('fecha_contratacion')
        empleado.save()
        return redirect('listar_empleados')
    return render(request, 'empleados/editar_empleado.html', {'empleado': empleado})

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('listar_empleados')
    return render(request, 'empleados/eliminar_empleado.html', {'empleado': empleado})