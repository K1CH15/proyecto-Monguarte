from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from compra.forms import CompraForm, CompraUpdateForm, Detalle_CompraForm, Detalle_CompraUpdateForm
from compra.models import Compra, Detalle_Compra
from inventario.models import Materia_Prima


# Create your views here.
# Creación COMPRA crear,listar,modificar,eliminar


def compra_crear(request):
    titulo = "Compra"
    mensaje = f'¡Hecho! Se ha añadido con éxito la {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save()  # Obtén el objeto de compra recién creado
            messages.success(request, mensaje)
            return redirect('detalle_compra', pk=compra.id)  # Utiliza 'compra.id' para redirigir
        else:
            messages.error(request, mensajeerror)
    else:
        form = CompraForm()

    context = {
        "titulo": titulo,
        "form": form,
    }

    return render(request, "compra/crear.html", context)


# @login_required
def compra_listar(request):
    titulo = "Compra"
    modulo = "compra"
    compra = Compra.objects.all()
    context = {
        "titulo": titulo,
        "modulo": modulo,
        "compra": compra,
    }
    return render(request, "compra/listar.html", context)


# @login_required
def compra_modificar(request, pk):
    titulo = "Compra"
    compra = Compra.objects.get(id=pk)
    mensaje = f'¡Hecho! La {titulo} se ha modificado exitosamente.'
    if request.method == 'POST':
        form = CompraUpdateForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('compra')
        else:
            messages.error(request, 'Error Al Modificar La Compra')
    else:
        form = CompraUpdateForm(instance=compra)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "compra/modificar.html", context)


# @login_required
def compra_eliminar(request, pk):
    compra = Compra.objects.filter(id=pk)
    compra.update(
        estado="0"
    )
    return redirect('compra')


# Creación DETALLE COMPRA
@login_required
def detalle_compra_crear(request):
    titulo = "Detalle Compra Crear"
    comprasn = Compra.objects.all()  # Obtén las compras desde la base de datos
    mensaje = f'¡Hecho! Se ha añadido con éxito el {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'
    if request.method == 'POST':
        form = Detalle_CompraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('detalle_compra')
        else:
            messages.error(request, mensajeerror)

    else:
        from inventario.models import Materia_Prima
        form = Detalle_CompraForm()
        materia_prima_activa = Materia_Prima.objects.filter(estado='1')
        form.fields['materia_prima'].queryset = materia_prima_activa
    context = {
        "titulo": titulo,
        "comprasn": comprasn,
        "form": form  # Agrega el formulario al contexto
    }

    return render(request, "detalle_compra/crear.html", context)


@login_required
def detalle_compra_listar(request, pk):
    titulo = "Detalle Compra"
    modulo = "compra"
    compra = Compra.objects.get(id=pk)
    m = Materia_Prima.objects.filter(estado="1")
    detalle_compra = Detalle_Compra.objects.filter(compra__id=pk)
    form = Detalle_CompraForm()  # Definir el formulario fuera del bloque if
    if request.method == "POST":
        materia_prima_id = request.POST.get('materia_prima')  # Obtén la materia prima del formulario POST
        cantidad = int(request.POST.get('cantidad', 0))  # Obtén la cantidad del formulario POST

        # Verifica si ya existe un registro con la misma materia prima en la compra actual
        detalle_existente = detalle_compra.filter(materia_prima=materia_prima_id).first()

        if detalle_existente:
            # Si existe, aumenta la cantidad en ese registro
            detalle_existente.cantidad += cantidad
            detalle_existente.save()
        else:
            # Si no existe, crea un nuevo registro
            form = Detalle_CompraForm(request.POST)
            if form.is_valid():
                det_compra = form.save(commit=False)
                det_compra.compra = Compra.objects.get(id=pk)
                det_compra.save()
                messages.success(request, "El formulario se ha enviado correctamente.")
            else:
                messages.error(request, "El formulario tiene errores.")
    else:
        form = Detalle_CompraForm()

    context = {
        "titulo": titulo,
        "modulo": modulo,
        "detalle_compras": detalle_compra,
        "compra": compra,
        "materias": m,
        "form": form
    }
    return render(request, "detalle_compra/listar.html", context)


@login_required
def detalle_compra_modificar(request, pk):
    titulo = "Detalle_compra"
    detalle_compra = Detalle_Compra.objects.get(id=pk)
    mensaje = f'¡Hecho! El {titulo} se ha modificado exitosamente.'
    if request.method == 'POST':
        form = Detalle_CompraUpdateForm(request.POST, instance=detalle_compra)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('detalle_compra')
        else:
            messages.error(request, 'Error Al Modificar El Detalle Compra')
    else:
        form = Detalle_CompraUpdateForm(instance=detalle_compra)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "detalle_compra/modificar.html", context)


def detalle_compra_finalizar(request, pk):
    try:
        compra = Compra.objects.get(id=pk)
    except Compra.DoesNotExist:
        # Maneja el caso en el que no se encuentra la compra
        return redirect('compra')

    # Verifica que la compra no esté ya finalizada
    if compra.estado != '0':
        # Cambia el estado de la compra a "Inactivo" (finalizado)
        compra.estado = '0'
        compra.save()

        # Itera a través de los detalles de compra asociados a esta compra
        for detalle_compra in Detalle_Compra.objects.filter(compra=compra):
            # Calcula el valor total multiplicando la cantidad y el precio unitario
            cantidad = detalle_compra.cantidad
            precio_unitario = detalle_compra.precio_unidad
            valor_total = cantidad * precio_unitario

            # Actualiza el valor total en el detalle de compra
            detalle_compra.valor_total = valor_total
            detalle_compra.save()

            # Actualiza el stock de la materia prima
            if detalle_compra.materia_prima:
                detalle_compra.materia_prima.stock += detalle_compra.cantidad
                detalle_compra.materia_prima.save()
                if detalle_compra.materia_prima:
                    if detalle_compra.materia_prima.precio_unitario != detalle_compra.precio_unidad:
                        detalle_compra.materia_prima.precio_unitario = detalle_compra.precio_unidad
                        detalle_compra.materia_prima.save()

        return redirect('compra')
    else:
        # La compra ya estaba finalizada
        return redirect('compra')


def verr_contenido(request, pk):
    compra = Compra.objects.get(pk=pk)
    detalle_compra = Detalle_Compra.objects.filter(compra=compra)  # Fetch related details
    context = {
        'titulo': 'Título de la Compra',
        'compra': compra,
        "detalle_compras": detalle_compra,  # Pass the details to the template
    }
    return render(request, 'compra/compra_final.html', context)


def aumentarr_cantidad(request, pk):
    detalle_compra = get_object_or_404(Detalle_Compra, id=pk)
    detalle_compra.cantidad += 1
    detalle_compra.save()
    return redirect('detalle_compra', pk=detalle_compra.compra.pk)


def disminuirr_cantidad(request, pk):
    detalle_compra = get_object_or_404(Detalle_Compra, id=pk)
    if detalle_compra.cantidad > 0:
        detalle_compra.cantidad -= 1
        detalle_compra.save()
    if detalle_compra.cantidad == 0:
        detalle_compra.delete()  # Delete the product if quantity reaches 0
    return redirect('detalle_compra', pk=detalle_compra.compra.pk)


def eliminar_detalle_compra(request, pk):
    detalle_compra = get_object_or_404(Detalle_Compra, id=pk)
    detalle_compra.delete()
    # Agregar un mensaje de advertencia
    messages.warning(request, 'El detalle de compra se ha eliminado con éxito.')

    return redirect('detalle_compra', pk=detalle_compra.compra.pk)
