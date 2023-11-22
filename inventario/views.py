from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from inventario.forms import FabricacionForm, FabricacionUptadeForm, Fabricacion, Fabricacion_DetalleForm
from inventario.forms import Materia_PrimaForm, Materia_PrimaUptadeForm
from inventario.models import Materia_Prima, Fabricacion_Detalle


# Create your views here.

# CRUD Materia Prima

@login_required
def materia_prima_crear(request):
    titulo = "materia prima"
    mensaje = f'¡Hecho! Se ha añadido con éxito la {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'
    if request.method == 'POST':
        form = Materia_PrimaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('materias-primas')
        else:
            messages.error(request, mensajeerror)

    else:
        form = Materia_PrimaForm()
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "materia prima/crear.html", context)


# @login_required
def materia_prima_listar(request):
    titulo = "Materia Prima"
    modulo = "inventarios"
    m = Materia_Prima.objects.all()
    context = {
        "titulo": titulo,
        "modulo": modulo,
        "materias": m,
    }
    return render(request, "materia prima/listar.html", context)


@login_required
def materia_prima_modificar(request, pk):
    titulo = "materia prima"
    mensaje = f'¡Hecho! La {titulo} se ha modificado exitosamente.'
    materia_prima = Materia_Prima.objects.get(id=pk)
    if request.method == 'POST':
        form = Materia_PrimaUptadeForm(request.POST, instance=materia_prima)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('materias-primas')
    else:
        form = Materia_PrimaUptadeForm(instance=materia_prima)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "materia prima/modificar.html", context)


@login_required
def materia_prima_eliminar(request, pk):
    materia_prima = Materia_Prima.objects.filter(id=pk)
    materia_prima.update(
        estado="0"
    )
    return redirect('materias-primas')


# CRUD Stock_Materia_Prima

@login_required
def fabricacion_crear(request):
    titulo = "Fabricación"
    mensaje = f'¡Hecho! Se ha añadido con éxito la {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'

    if request.method == 'POST':
        form = FabricacionForm(request.POST)
        if form.is_valid():
            fabricacion = form.save()  # Guardar la fabricación

            messages.success(request, mensaje)
            return redirect("fabricacion_detalle", pk=fabricacion.id)

        else:
            messages.error(request, mensajeerror)

    else:
        form = FabricacionForm()
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "fabricacion/crear.html", context)


@login_required
def fabricacion_listar(request):
    titulo = "Fabricacion"
    modulo = "inventarios"
    fabricacion = Fabricacion.objects.all()
    context = {
        "titulo": titulo,
        "modulo": modulo,
        "fabricacion": fabricacion,
    }
    return render(request, "fabricacion/listar.html", context)


@login_required
def fabricacion_modificar(request, pk):
    titulo = "Fabricacion"
    mensaje = f'¡Hecho! La {titulo} se ha modificado exitosamente.'
    fabricacion = Fabricacion.objects.get(id=pk)
    if request.method == 'POST':
        form = FabricacionUptadeForm(request.POST, instance=fabricacion)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('fabricaciones')
    else:
        form = FabricacionUptadeForm(instance=fabricacion)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "fabricacion/modificar.html", context)


@login_required
def fabricacion_eliminar(request, pk):
    fabricacion = Fabricacion.objects.filter(id=pk)
    fabricacion.update(
        estado="0"
    )
    return redirect('fabricaciones')


def fabricacion_detalle_listar(request, pk):
    titulo = "Fabricacion"
    modulo = "inventarios"
    fabricacion = Fabricacion.objects.get(id=pk)
    m = Materia_Prima.objects.filter(estado="1")
    fabricacion_detalle = Fabricacion_Detalle.objects.filter(fabricacion__id=pk)  # Editar?

    if request.method == "POST":
        materia_prima_id = request.POST.get('materia_prima')  # Obtén la materia prima del formulario POST
        cantidad_materia = int(request.POST.get('cantidad_materia', 0))  # Obtén la cantidad del formulario POST

        # Verifica si ya existe un registro con la misma materia prima en la compra actual
        detalle_existente = fabricacion_detalle.filter(materia_prima=materia_prima_id).first()
        if detalle_existente:
            # Si existe, aumenta la cantidad en ese registro
            detalle_existente.cantidad_materia += cantidad_materia
            detalle_existente.save()
        else:

            form = Fabricacion_DetalleForm(request.POST)
            if form.is_valid():
                det_fabricacion = form.save(commit=False)
                det_fabricacion.fabricacion = Fabricacion.objects.get(id=pk)
                det_fabricacion.save()
                messages.success(request, "El formulario se ha enviado correctamente.")
            else:
                messages.error(request, "El formulario tiene errores.")
    else:
        form = Fabricacion_DetalleForm()
    context = {
        "titulo": titulo,
        "modulo": modulo,
        "fabricacion": fabricacion,
        "fabricacion_detalles": fabricacion_detalle,
        "materias": m,
    }
    return render(request, "fabricacion_detalle/listar.html", context)


def fabricacion_detalle_finalizar(request, pk):
    try:
        fabricacion = Fabricacion.objects.get(id=pk)
    except Fabricacion.DoesNotExist:
        return redirect('fabricaciones')

    if fabricacion.estado != '0':
        costo_fabricacion_total = Decimal(0)

        # Itera a través de los detalles de Fabricacion_Detalle relacionados con la fabricacion
        for fabricacion_detalle in Fabricacion_Detalle.objects.filter(fabricacion=fabricacion):
            if fabricacion_detalle.materia_prima:
                fabricacion_detalle.materia_prima.stock -= fabricacion_detalle.cantidad_materia
                fabricacion_detalle.materia_prima.save()

                # Llama al método calcular_costo_fabricacion en instancias de Fabricacion_Detalle
                costo_unitario = fabricacion_detalle.calcular_costo_fabricacion()
                costo_fabricacion_total += costo_unitario

        fabricacion.costo_fabricacion = costo_fabricacion_total
        fabricacion.estado = '0'
        fabricacion.save()
        # Asignar el costo de fabricación al producto
        fabricacion.producto.costo_fabricacion = costo_fabricacion_total
        fabricacion.producto.stock += fabricacion.cantidad_producto
        fabricacion.producto.save()

        return redirect('fabricaciones')

    else:
        return redirect('fabricaciones')


def verr_contenido(request, pk):
    fabricacion = Fabricacion.objects.get(pk=pk)
    fabricacion_detalle = Fabricacion_Detalle.objects.filter(fabricacion=fabricacion)  # Fetch related details
    context = {
        'titulo': 'Título de la Compra',
        'fabricacion': fabricacion,
        "fabricacion_detalles": fabricacion_detalle,  # Pass the details to the template
    }
    return render(request, 'fabricacion/fabricacion_final.html', context)


def aumentarr_cantidad(request, pk):
    fabricacion_detalle = get_object_or_404(Fabricacion_Detalle, id=pk)
    fabricacion_detalle.cantidad_materia += 1
    fabricacion_detalle.save()
    return redirect('fabricacion_detalle', pk=fabricacion_detalle.fabricacion.pk)


def disminuirr_cantidad(request, pk):
    fabricacion_detalle = get_object_or_404(Fabricacion_Detalle, id=pk)
    if fabricacion_detalle.cantidad_materia > 0:
        fabricacion_detalle.cantidad_materia -= 1
        fabricacion_detalle.save()
    if fabricacion_detalle.cantidad_materia == 0:
        fabricacion_detalle.delete()  # Delete the product if quantity reaches 0
    return redirect('fabricacion_detalle', pk=fabricacion_detalle.fabricacion.pk)


def eliminarr_fabricacion_detalle(request, pk):
    fabricacion_detalle = get_object_or_404(Fabricacion_Detalle, id=pk)
    fabricacion_detalle.delete()
    # Agregar un mensaje de advertencia
    messages.warning(request, 'El detalle de compra se ha eliminado con éxito.')

    return redirect('fabricacion_detalle', pk=fabricacion_detalle.fabricacion.pk)

# def listar_stock(request):
#     titulo = "Stock"
#     modulo = "inventarios"
#     stock = Stock.objects.all()
#     context = {
#         "titulo": titulo,
#         "modulo": modulo,
#         "stock": stock,
#     }
#     return render(request, 'stock/listar_stock.html', context)
#
# def agregar_stock(request):
#     if request.method == 'POST':
#         form = StockForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('stock:listar_stock')
#
#     else:
#         form = StockForm()
#
#     return render(request, 'stock/listar_stock.html', {'form': form})
