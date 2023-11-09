from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from productos.forms import ProductoForm, ProductoUpdateForm
from productos.models import Producto
from django.shortcuts import render, get_object_or_404
from .forms import PrecioUnitarioForm


# Create your views here.
@login_required
def producto_crear(request):
    titulo = "Producto"
    mensaje = f'¡Hecho! Se ha añadido con éxito el {titulo}.'
    mensajeerror = f'¡Oops! Hubo un error en el formulario de {titulo}. Por favor, revisa y corrige los campos resaltados en rojo.'
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)

            return redirect('productosl')
        else:
            messages.error(request,mensajeerror)
    else:
        form = ProductoForm()
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "productos/crear.html", context)

@login_required
def producto_listar(request):
    titulo = "Producto"
    modulo = "productos"
    productosn = Producto.objects.all()
    context = {
        "titulo": titulo,
        "modulo": modulo,
        "productos": productosn
    }
    return render(request, "productos/listar.html", context)

@login_required
def producto_modificar(request, pk):
    titulo = "Producto"
    producto = Producto.objects.get(id=pk)
    mensaje = f'¡Hecho! El {titulo} se ha modificado exitosamente.'
    if request.method == 'POST':
        form = ProductoUpdateForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, mensaje)
            return redirect('productosl')
    else:
        form = ProductoUpdateForm(instance=producto)
    context = {
        "titulo": titulo,
        "form": form
    }
    return render(request, "productos/modificar.html", context)

@login_required
def producto_eliminar(request, pk):
    mensaje = f'¡Hecho! El P se ha modificado exitosamente.'
    producto = Producto.objects.filter(id=pk)
    producto.update(
        estado="0",
    )
    messages.info(request, '¡Hecho! El Producto se ha eliminado exitosamente.')

    return redirect('productosl')

def lista_de_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar.html', {'productos': productos})

def establecer_precio(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = PrecioUnitarioForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_de_productos')  # Redirige a la lista de productos después de guardar el precio
    else:
        form = PrecioUnitarioForm(instance=producto)

    return render(request, 'productos/editar_precio.html', {'form': form, 'producto': producto})
# def tamaño_crear(request):
#     titulo="Tamaño"
#     if request.method== 'POST':
#         form= TamañoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'correcto,el formulario esta completado')
#
#             return redirect('tamaños')
#         else:
#              messages.error(request,'¡Oops! Parece que ha ocurrido un error en el formulario. Te pedimos que revises los campos resaltados y realices las correcciones necesarias.')
#     else:
#         form= TamañoForm()
#     context={
#         "titulo":titulo,
#         "form":form
#         }
#     return render(request,"tamaños/crear.html", context)
#
# def tamaño_listar(request):
#     titulo="tamaño"
#     modulo="productos"
#     tamaños= Tamaño.objects.all()
#     context={
#         "titulo":titulo,
#         "modulo":modulo,
#         "tamaños":tamaños,
#     }
#     return render(request,"tamaños/listar.html", context)
#
# def tamaño_modificar(request,pk):
#     titulo="Tamaño"
#     tamaño= Tamaño.objects.get(id=pk)
#
#     if request.method== 'POST':
#         form= TamañoUpdateForm(request.POST, instance=tamaño)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'El formulario se ha enviado correctamente.')
#             return redirect('tamaños')
#         else:
#             messages.error(request, 'Error Al Modificar La Compra')
#     else:
#         form= TamañoUpdateForm(instance=tamaño)
#     context={
#         "titulo":titulo,
#         "form":form
#         }
#     return render(request,"tamaños/modificar.html", context)
#
# def tamaño_eliminar(request,pk):
#     tamaño= Tamaño.objects.filter(id=pk)
#     tamaño.update(
#         estado="0"
#     )
#     return redirect('tamaños')
#
# def tipo_crear(request):
#     titulo="Tipo"
#     if request.method== 'POST':
#         form= TipoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'El formulario de tipo se ha enviado correctamente.')
#             return redirect('tipos')
#         else:
#             messages.error(request,'¡Oops! Parece que ha ocurrido un error en el formulario. Te pedimos que revises los campos resaltados y realices las correcciones necesarias.')
#     else:
#         form= TipoForm()
#     context={
#         "titulo":titulo,
#         "form":form
#         }
#     return render(request,"tipos/crear.html", context)
#
# def tipo_listar(request):
#     titulo="Tipo"
#     modulo="Productos"
#     tipos= Tipo.objects.all()
#     context={
#         "titulo":titulo,
#         "modulo":modulo,
#         "tipos":tipos
#     }
#     return render(request,"tipos/listar.html", context)
#
# def tipo_modificar(request,pk):
#     titulo="Tipo"
#
#     tipo= Tipo.objects.get(id=pk)
#
#     if request.method== 'POST':
#         form= TipoUpdateForm(request.POST, instance=tipo)
#         if form.is_valid():
#             form.save()
#             return redirect('tipos')
#     else:
#         form= TipoUpdateForm(instance=tipo)
#     context={
#         "titulo":titulo,
#         "form":form
#         }
#     return render(request,"tipos/modificar.html", context)
# def tipo_eliminar(request,pk):
#     tipo= Tipo.objects.filter(id=pk)
#     tipo.update(
#         estado="0"
#     )
#     return redirect('tipos')
