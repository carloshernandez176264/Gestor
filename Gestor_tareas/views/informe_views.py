import random
from collections import defaultdict

from django.shortcuts import render
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
    facturas = Factura.objects.all()
    for factura in facturas:
        if factura.fecha_emision:
            anio = factura.fecha_emision.year
            facturacion_anual[anio] += float(factura.total)
        if factura.cliente:
            facturacion_por_cliente[factura.cliente.nombre] += float(factura.total)
            empleados_por_cliente[factura.cliente.nombre].add(factura.empleado)
        if factura.empleado:
            facturacion_empleados[factura.empleado.nombre] += float(factura.total)

    # Gráfico de porcentajes por cliente
    clientes = list(facturacion_por_cliente.keys())
    totales_clientes = list(facturacion_por_cliente.values())
    colores_clientes = [f"#{''.join(random.choices('0123456789ABCDEF', k=6))}" for _ in clientes]

    plt.figure(figsize=(8, 8))
    plt.pie(totales_clientes, labels=clientes, autopct='%1.1f%%', startangle=140, colors=colores_clientes)
    plt.title('Porcentaje de Facturación por Cliente')
    plt.tight_layout()

    buffer_pie = io.BytesIO()
    plt.savefig(buffer_pie, format='png')
    buffer_pie.seek(0)
    grafico_porcentajes_cliente = base64.b64encode(buffer_pie.getvalue()).decode('utf-8')
    buffer_pie.close()
    plt.close()

    # Comparativo anual en porcentaje
    anios = sorted(facturacion_anual.keys())
    totales_anuales = [facturacion_anual[anio] for anio in anios]
    total_global = sum(totales_anuales)
    porcentajes_anuales = [(total / total_global) * 100 for total in totales_anuales]

    plt.figure(figsize=(10, 6))
    plt.bar(anios, porcentajes_anuales, color='skyblue')
    plt.xlabel('Año')
    plt.ylabel('Porcentaje del Total')
    plt.title('Comparación Anual en Porcentaje')
    plt.tight_layout()

    buffer_anual = io.BytesIO()
    plt.savefig(buffer_anual, format='png')
    buffer_anual.seek(0)
    grafico_comparativo_anual = base64.b64encode(buffer_anual.getvalue()).decode('utf-8')
    buffer_anual.close()
    plt.close()

    # Gráfico de facturación por empleado
    empleados = list(facturacion_empleados.keys())
    totales_empleados = list(facturacion_empleados.values())

    plt.figure(figsize=(10, 6))
    plt.barh(empleados, totales_empleados, color='purple')
    plt.xlabel('Facturación Total')
    plt.ylabel('Empleado')
    plt.title('Facturación por Empleado')
    plt.tight_layout()

    buffer_empleados = io.BytesIO()
    plt.savefig(buffer_empleados, format='png')
    buffer_empleados.seek(0)
    grafico_empleados = base64.b64encode(buffer_empleados.getvalue()).decode('utf-8')
    buffer_empleados.close()
    plt.close()

    # Número de empleados por cliente
    empleados_totales = [len(empleados_por_cliente[cliente]) for cliente in clientes]

    plt.figure(figsize=(10, 6))
    plt.bar(clientes, empleados_totales, color='orange')
    plt.xlabel('Cliente')
    plt.ylabel('Número de Empleados')
    plt.title('Cantidad de Empleados por Cliente')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer_clientes = io.BytesIO()
    plt.savefig(buffer_clientes, format='png')
    buffer_clientes.seek(0)
    grafico_clientes = base64.b64encode(buffer_clientes.getvalue()).decode('utf-8')
    buffer_clientes.close()
    plt.close()

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