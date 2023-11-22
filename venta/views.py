from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from productos.models import Producto
from usuario.models import Comision
from venta.forms import Detalle_VentaForm, Detalle_VentaUpdateForm, VentaForm, VentaUpdateForm
from venta.models import Venta, Detalle_Venta


# Create your views here.
# VIEWS VENTA

# @login_required
def venta_crear(request):
    titulo = "Venta"
    mensaje = f'¡Hecho! Se ha añadido con éxito la {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save()
            messages.success(request, mensaje)
            return redirect('detalle_ventas', pk=venta.id)
        else:
            messages.error(request, mensajeerror)
    else:
        form = VentaForm()
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "venta/crear.html", context)


# @login_required
def venta_listar(request):
    titulo = "Venta"
    modulo = "ventas"
    venta = Venta.objects.all()
    context = {"titulo": titulo, "venta": venta, "modulo": modulo}
    return render(request, "venta/listar.html", context)


# @login_required
def venta_modificar(request, pk):
    titulo = "Venta"
    mensaje = f'¡Hecho! La {titulo} se ha modificado exitosamente.'
    venta = Venta.objects.get(id=pk)

    if request.method == 'POST':
        form = VentaUpdateForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('ventas')
    else:
        form = VentaUpdateForm(instance=venta)
    context = {"titulo": titulo, "form": form}
    return render(request, "venta/modificar.html", context)


# @login_required
def venta_eliminar(request, pk):
    venta = Venta.objects.filter(id=pk)
    venta.update(estado="0")
    return redirect('ventas')


# VIEWS DETALLE_VENTA

# @login_required
def detalle_venta_crear(request):
    titulo = "Detalle Venta"
    mensaje = f'¡Hecho! Se ha añadido con éxito el {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'

    if request.method == 'POST':
        form = Detalle_VentaForm(request.POST)
        if form.is_valid():
            cantidad_total = form.cleaned_data['cantidad_total']
            producto_stock = form.cleaned_data['producto'].stock

            if cantidad_total > producto_stock:
                messages.error(request,
                               f'No hay suficiente stock del producto disponible. Cantidad en stock: {producto_stock}')
            else:
                form.save()
                messages.success(request, mensaje)
                return redirect('detalle_ventas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            messages.error(request, mensajeerror)

    else:
        from productos.models import Producto
        form = Detalle_VentaForm()
        producto_activa = Producto.objects.filter(estado='1')
        form.fields['producto'].queryset = producto_activa
    context = {"titulo": titulo, "form": form}
    return render(request, "detalle_venta/crear.html", context)


# @login_required
def detalle_venta_listar(request, pk):
    titulo = "Detalle Venta"
    modulo = "venta"
    venta = Venta.objects.get(id=pk)
    productosn = Producto.objects.filter(estado="1")
    detalle_venta = Detalle_Venta.objects.filter(venta__id=pk)
    form = Detalle_VentaForm()  # Definir el formulario fuera del bloque if

    if request.method == "POST":
        productos_id = request.POST.get('producto')  # Obtén el producto del formulario POST
        cantidad_total = int(request.POST.get('cantidad_total', 0))  # Obtén la cantidad del formulario POST

        # Verifica si el precio unitario del producto está definido
        producto = Producto.objects.get(id=productos_id)
        if producto.precio_unitario is None:
            messages.warning(request, 'El precio unitario no está definido para este producto.')
        else:
            # Continúa con la lógica de agregar el detalle de venta
            detalle_existente = detalle_venta.filter(producto=productos_id).first()

            if detalle_existente:
                # Si existe, aumenta la cantidad en ese registro
                detalle_existente.cantidad_total += cantidad_total
                detalle_existente.save()
            else:
                # Si no existe, crea un nuevo registro
                form = Detalle_VentaForm(request.POST)
                if form.is_valid():
                    det_venta = form.save(commit=False)
                    det_venta.venta = Venta.objects.get(id=pk)

                    # Verifica el stock disponible antes de guardar
                    if cantidad_total <= producto.stock:
                        det_venta.save()
                        messages.success(request, "El formulario se ha enviado correctamente.")
                    else:
                        messages.error(request,
                                       f"No hay suficiente stock del producto disponible. Cantidad en stock: {producto.stock}")
                else:
                    messages.error(request, "El formulario tiene errores.")
    else:
        form = Detalle_VentaForm()

    context = {
        "titulo": titulo,
        "modulo": modulo,
        "detalle_ventas": detalle_venta,
        "venta": venta,
        "productos": productosn,
        "form": form
    }
    return render(request, "detalle_venta/listar.html", context)


# @login_required
def detalle_venta_modificar(request, pk):
    titulo = "Detalle Venta"
    mensaje = f'¡Hecho! El {titulo} se ha modificado exitosamente.'
    detalle_venta = Detalle_Venta.objects.get(id=pk)
    if request.method == 'POST':
        form = Detalle_VentaUpdateForm(request.POST, instance=detalle_venta)
        if form.is_valid():
            form.save()
            return redirect('detalle_ventas')
    else:
        form = Detalle_VentaUpdateForm(instance=detalle_venta)
    context = {"titulo": titulo, "form": form}
    return render(request, "detalle_venta/modificar.html", context)


def detalle_ventas_finalizar(request, pk):
    try:
        venta = Venta.objects.get(id=pk)
    except Venta.DoesNotExist:
        # Maneja el caso en el que no se encuentra la venta
        return redirect('ventas')

    # Verifica que la venta no esté ya finalizada
    if venta.estado != '0':
        # Cambia el estado de la compra a "Inactivo" (finalizado)
        venta.estado = '0'
        venta.save()

        # Calcula y resta la comisión del stock solo cuando se finaliza la venta
        detalles_venta = Detalle_Venta.objects.filter(venta=venta)
        for detalle in detalles_venta:
            detalle.valor_total = detalle.precio_unitario() * detalle.cantidad_total
            detalle.save()

            comision_valor = detalle.valor_total * Decimal('0.10')  # Calcula el 10% de la comisión

            # Crea una instancia de Comision asociada con el detalle de venta actual
            comision = Comision.objects.create(valor_comision=comision_valor)

            # Resta la cantidad_total del detalle del stock del producto
            detalle.producto.stock -= detalle.cantidad_total
            detalle.producto.save()

        return redirect('ventas')
    else:
        # La venta ya estaba finalizada
        return redirect('ventas')


def ver_contenido(request, pk):
    venta = Venta.objects.get(pk=pk)
    detalle_venta = Detalle_Venta.objects.filter(venta=venta)  # Fetch related details
    context = {
        'titulo': 'Título de la Venta',
        'venta': venta,
        "detalle_ventas": detalle_venta,  # Pass the details to the template
    }
    return render(request, 'venta/venta_final.html', context)


def aumentar_cantidad(request, pk):
    detalle_venta = get_object_or_404(Detalle_Venta, id=pk)
    detalle_venta.cantidad_total += 1
    detalle_venta.save()
    return redirect('detalle_ventas', pk=detalle_venta.venta.pk)


def disminuir_cantidad(request, pk):
    detalle_venta = get_object_or_404(Detalle_Venta, id=pk)
    if detalle_venta.cantidad_total > 0:
        detalle_venta.cantidad_total -= 1
        detalle_venta.save()
    if detalle_venta.cantidad_total == 0:
        detalle_venta.delete()  # Delete the product if quantity reaches 0
    return redirect('detalle_ventas', pk=detalle_venta.venta.pk)


def eliminar_detalle_venta(request, pk):
    detalle_venta = get_object_or_404(Detalle_Venta, id=pk)
    detalle_venta.delete()
    # Agregar un mensaje de advertencia
    messages.warning(request, 'El detalle de compra se ha eliminado con éxito.')

    return redirect('detalle_ventas', pk=detalle_venta.venta.pk)
