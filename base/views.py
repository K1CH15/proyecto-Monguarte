from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from compra.models import Compra,Detalle_Compra
from venta.models import Venta,Detalle_Venta
from inventario.models import Materia_Prima,Fabricacion
from productos.models import Producto
from usuario.models import Persona,Comision
@login_required
def principal(request):
    titulo="Bienvenido"
    compras= Compra.objects.all().count
    detalle_compras=Detalle_Compra.objects.all().count()
    ventas=Venta.objects.all().count()
    detalle_ventas=Detalle_Venta.objects.all().count()
    materias_primas=Materia_Prima.objects.all().count()
    productos=Producto.objects.all().count()
    personas=Persona.objects.all().count()
    comisiones=Comision.objects.all().count()
    fabricaciones=Fabricacion.objects.all().count()



    context={
        "titulo":titulo,
        "compras":compras,
        "detalle_compras":detalle_compras,
        "ventas":ventas,
        "detalle_ventas":detalle_ventas,
        "materias_primas":materias_primas,
        "productos":productos,
        "personas":personas,
        "comisiones":comisiones,
        "fabricaciones":fabricaciones,


    }
    return render(request,"index.html",context)

def logout_user(request):
    logout(request)
    return redirect('inicio')
#modulos
def usuario_vista (request):
    titulo="usuarios"
    context={

        "titulo":titulo,
    }
    return render(request,"partials/usuario.html",context)
def compra_vista (request):
    titulo="compras"
    context={

        "titulo":titulo,
    }
    return render(request,"partials/compra.html",context)

def inventario_vista (request):
    titulo="Inventarios"
    context={

        "titulo":titulo,
    }
    return render(request,"partials/inventario.html",context)

def venta_vista (request):
    titulo="ventas"
    context={

        "titulo":titulo,
    }
    return render(request,"partials/venta.html",context)

def producto_vista (request):
    titulo="productos"
    context={

        "titulo":titulo,
    }
    return render(request,"partials/producto.html",context)

def accessibility (request):

    return render(request,"partials/accessibility.html")

