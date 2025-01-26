from django.shortcuts import render, redirect, get_object_or_404
from Gestor_tareas.models import Empleado, Cliente


def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/listar_empleados.html', {'empleados': empleados})


def agregar_empleado(request):
    clientes = Cliente.objects.all()
    error = None

    if request.method == 'POST':
        try:
            # Recoger datos del formulario
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            puesto = request.POST.get('puesto')
            salario = request.POST.get('salario')
            fecha_contratacion = request.POST.get('fecha_contratacion')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            numero_identificacion = request.POST.get('numero_identificacion')
            cliente_id = request.POST.get('cliente')
            activo = request.POST.get('activo') == "True"
            fecha_termino = request.POST.get('fecha_termino')
            notas = request.POST.get('notas')

            # Validación: cliente debe existir
            cliente = get_object_or_404(Cliente, id=cliente_id)

            # Crear empleado
            empleado = Empleado(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                direccion=direccion,
                puesto=puesto,
                salario=salario,
                fecha_contratacion=fecha_contratacion,
                fecha_nacimiento=fecha_nacimiento,
                numero_identificacion=numero_identificacion,
                cliente=cliente,
                activo=activo,
                fecha_termino=fecha_termino,
                notas=notas,
            )
            empleado.full_clean()  # Valida los datos antes de guardar
            empleado.save()

            return redirect('listar_empleados')

        except Cliente.DoesNotExist:
            error = "El cliente seleccionado no existe."
        except Exception as e:
            error = f"Ocurrió un error: {str(e)}"

    return render(request, 'empleados/agregar_empleado.html', {
        'clientes': clientes,
        'error': error,
    })

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