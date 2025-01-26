from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from Gestor_tareas.models import Factura, Cliente, Empleado

@login_required
def agregar_factura(request):
    clientes = Cliente.objects.all()
    empleados_filtrados = Empleado.objects.none()  # Ningún empleado por defecto

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        empleado_id = request.POST.get('empleado_id')
        numero_factura = request.POST.get('numero_factura')
        fecha_emision = request.POST.get('fecha_emision')
        total = request.POST.get('total')

        # Validación
        try:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            empleado = get_object_or_404(Empleado, id=empleado_id, cliente=cliente)

            # Crear factura
            Factura.objects.create(
                cliente=cliente,
                empleado=empleado,
                numero_factura=numero_factura,
                fecha_emision=fecha_emision,
                total=total,
            )
            return redirect('listar_facturas')
        except Exception as e:
            return render(
                request,
                'facturas/agregar_factura.html',
                {'clientes': clientes, 'empleados': empleados_filtrados, 'error': str(e)},
            )

    # Filtro por cliente en GET
    cliente_id = request.GET.get('cliente_id')
    if cliente_id:
        empleados_filtrados = Empleado.objects.filter(cliente_id=cliente_id)

    return render(request, 'facturas/agregar_factura.html', {'clientes': clientes, 'empleados': empleados_filtrados})

@login_required
def editar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        factura.total = request.POST.get('total')
        factura.save()
        return redirect('listar_facturas')
    return render(request, 'facturas/editar_factura.html', {'factura': factura})

@login_required
def eliminar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        factura.delete()
        return redirect('listar_facturas')
    return render(request, 'facturas/eliminar_factura.html', {'factura': factura})

@login_required
def listar_facturas(request):
    facturas = Factura.objects.select_related('empleado', 'cliente').all()  # Optimiza la consulta
    return render(request, 'facturas/listar_facturas.html', {'facturas': facturas})

@login_required
def listar_facturas_empleado(request):

    empleado = request.user.empleado  # Suponiendo que el usuario autenticado está relacionado con el modelo Empleado
    if not empleado:
        return render(request, 'error.html', {'mensaje': 'Empleado no encontrado.'})

    facturas = Factura.objects.filter(cliente=empleado.cliente)  # Filtra las facturas por cliente del empleado
    return render(request, 'facturas/listar_facturas.html', {'facturas': facturas})