import random
from collections import defaultdict

from django.shortcuts import render
from matplotlib import cm

from Gestor_tareas.models import Factura
import matplotlib.pyplot as plt
import io
import urllib
import base64
import openpyxl
from django.http import HttpResponse

def generar_informe(request):
    # Inicializar contenedores de datos
    facturacion_por_cliente = defaultdict(float)
    facturacion_anual = defaultdict(float)
    empleados_por_cliente = defaultdict(set)
    facturacion_empleados = defaultdict(float)

    # Procesar facturas
    facturas = Factura.objects.select_related('cliente', 'empleado').all()
    for factura in facturas:
        if factura.fecha_emision:
            anio = factura.fecha_emision.year
            facturacion_anual[anio] += float(factura.total)
        if factura.cliente:
            facturacion_por_cliente[factura.cliente.nombre] += float(factura.total)
            empleados_por_cliente[factura.cliente.nombre].add(factura.empleado)
        if factura.empleado:
            facturacion_empleados[factura.empleado.nombre] += float(factura.total)

    # Gráfico 1: Porcentaje de Facturación por Cliente
    clientes = list(facturacion_por_cliente.keys())
    totales_clientes = list(facturacion_por_cliente.values())
    colores_clientes = cm.get_cmap('tab10')(range(len(clientes)))  # Usar colores de la paleta `tab10`

    plt.figure(figsize=(8, 8))
    plt.pie(
        totales_clientes,
        labels=clientes,
        autopct=lambda p: f'{p:.1f}%\n({p * sum(totales_clientes) / 100:.2f})',
        startangle=90,
        colors=colores_clientes,
        wedgeprops={'edgecolor': 'black'}  # Borde para mayor claridad
    )
    plt.title('Porcentaje de Facturación por Cliente', fontsize=14)
    plt.tight_layout()

    # Guardar gráfico
    buffer_pie = io.BytesIO()
    plt.savefig(buffer_pie, format='png')
    plt.close()
    buffer_pie.seek(0)
    grafico_porcentajes_cliente = base64.b64encode(buffer_pie.getvalue()).decode('utf-8')
    buffer_pie.close()

    # Gráfico 2: Comparación Anual
    anios = sorted(facturacion_anual.keys())
    totales_anuales = [facturacion_anual[anio] for anio in anios]
    plt.figure(figsize=(10, 6))
    plt.bar(anios, totales_anuales, color='lightblue', edgecolor='blue')
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Total Facturado ($)', fontsize=12)
    plt.title('Comparación de Facturación Anual', fontsize=14)
    plt.xticks(anios)
    for i, total in enumerate(totales_anuales):
        plt.text(i, total, f'{total:.2f}', ha='center', va='bottom')
    buffer_anual = io.BytesIO()
    plt.savefig(buffer_anual, format='png')
    plt.close()
    buffer_anual.seek(0)
    grafico_comparativo_anual = base64.b64encode(buffer_anual.getvalue()).decode('utf-8')
    buffer_anual.close()

    # Gráfico 3: Facturación por Empleado
    empleados = list(facturacion_empleados.keys())
    totales_empleados = list(facturacion_empleados.values())
    plt.figure(figsize=(10, 6))
    plt.barh(empleados, totales_empleados, color='purple', edgecolor='black')
    plt.xlabel('Facturación Total ($)', fontsize=12)
    plt.ylabel('Empleado', fontsize=12)
    plt.title('Facturación por Empleado', fontsize=14)
    for i, total in enumerate(totales_empleados):
        plt.text(total, i, f'{total:.2f}', va='center')
    buffer_empleados = io.BytesIO()
    plt.savefig(buffer_empleados, format='png')
    plt.close()
    buffer_empleados.seek(0)
    grafico_empleados = base64.b64encode(buffer_empleados.getvalue()).decode('utf-8')
    buffer_empleados.close()

    # Gráfico 4: Cantidad de Empleados por Cliente
    empleados_totales = [len(empleados_por_cliente[cliente]) for cliente in clientes]
    plt.figure(figsize=(10, 6))
    plt.bar(clientes, empleados_totales, color='orange', edgecolor='black')
    plt.xlabel('Cliente', fontsize=12)
    plt.ylabel('Cantidad de Empleados', fontsize=12)
    plt.title('Cantidad de Empleados por Cliente', fontsize=14)
    plt.xticks(rotation=45)
    buffer_clientes = io.BytesIO()
    plt.savefig(buffer_clientes, format='png')
    plt.close()
    buffer_clientes.seek(0)
    grafico_clientes = base64.b64encode(buffer_clientes.getvalue()).decode('utf-8')
    buffer_clientes.close()

    # Renderizar datos y gráficos
    return render(request, 'reportes/informes.html', {
        'grafico_porcentajes_cliente': grafico_porcentajes_cliente,
        'grafico_comparativo_anual': grafico_comparativo_anual,
        'grafico_empleados': grafico_empleados,
        'grafico_clientes': grafico_clientes,
        'facturacion_anual': dict(facturacion_anual),
        'facturacion_por_cliente': dict(facturacion_por_cliente),
    })

def exportar_informe(request):
    # Crear un libro de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Informe Gerencial"

    # Títulos de las columnas
    ws.append(["Cliente", "Empleado", "Fecha", "Número de Factura", "Total"])

    # Agregar datos de las facturas
    facturas = Factura.objects.all()
    for factura in facturas:
        ws.append([
            factura.cliente.nombre,
            factura.empleado.nombre,
            factura.fecha_emision.strftime('%Y-%m-%d') if factura.fecha_emision else "No definida",
            factura.numero_factura,
            float(factura.total),
        ])

    # Responder con el archivo Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="informe_gerencial.xlsx"'
    wb.save(response)
    return response