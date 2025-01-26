from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Gestor_tareas.models import Cliente


@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contacto = request.POST.get('contacto')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')

        Cliente.objects.create(
            nombre=nombre,
            contacto=contacto,
            direccion=direccion,
            email=email
        )
        return redirect('listar_clientes')
    return render(request, 'clientes/agregar_cliente.html')
@login_required
def editar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.contacto = request.POST.get('contacto')
        cliente.direccion = request.POST.get('direccion')
        cliente.email = request.POST.get('email')
        cliente.save()
        return redirect('listar_clientes')
    return render(request, 'clientes/editar_cliente.html', {'cliente': cliente})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.delete()
    return redirect('listar_clientes')
