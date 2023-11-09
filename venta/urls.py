from django.urls import path
from venta.views import venta_crear, venta_listar, venta_modificar, venta_eliminar, detalle_venta_crear, \
    detalle_venta_listar, detalle_venta_modificar, detalle_ventas_finalizar
from . import views

urlpatterns = [
    path('venta/', venta_listar, name="ventas"),
    path('venta/crear/', venta_crear, name="ventas-crear"),
    path('venta/modificar/<int:pk>/', venta_modificar, name="ventas-modificar"),
    path('venta/eliminar/<int:pk>/', venta_eliminar, name="ventas-eliminar"),

    path('detalle_venta/', detalle_venta_listar, name="detalle_ventas"),
    path('detalle_venta/crear/', detalle_venta_crear, name="detalle_venta-crear"),
    path('detalle_venta/modificar/<int:pk>/', detalle_venta_modificar, name="detalle_venta-modificar"),
    path('ventas/detalle_venta/<int:pk>/', views.detalle_venta_listar, name='detalle_ventas'),
    path('venta/finalizar/<int:pk>/', detalle_ventas_finalizar, name='venta-finalizar'),
    path('ver_contenido/<int:pk>/', views.ver_contenido, name='ver_contenido'),
    path('ventas/aumentar_cantidad/<int:pk>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('ventas/disminuir_cantidad/<int:pk>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('ventas/eliminar_detalle_compra/<int:pk>/eliminar/', views.eliminar_detalle_venta,
         name='eliminar_detalle_venta'),

]
