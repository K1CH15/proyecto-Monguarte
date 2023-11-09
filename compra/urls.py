from django.urls import path
from . import views

from compra.views import compra_listar, compra_crear, compra_modificar, compra_eliminar, detalle_compra_listar, \
    detalle_compra_crear, detalle_compra_modificar, detalle_compra_finalizar

urlpatterns = [
    path('compra/', compra_listar, name="compra"),
    path('compra/crear/', compra_crear, name="compra-crear"),
    path('compra/modificar/<int:pk>/', compra_modificar, name="compra-modificar"),
    path('compra/eliminar/<int:pk>/', compra_eliminar, name="compra-eliminar"),

    path('detalle_compra/<int:pk>/', detalle_compra_listar, name="detalle_compra"),
    path('detalle_compra/crear/', detalle_compra_crear, name="detalle_compra-crear"),
    path('detalle_compra/modificar/<int:pk>/', detalle_compra_modificar, name="detalle_compra-modificar"),
    path('compras/detalle_compra/<int:pk>/', views.detalle_compra_listar, name='detalle_compra'),
    path('finalizar/<int:pk>/', detalle_compra_finalizar, name='compra-finalizar'),
    path('verr_contenido/<int:pk>/', views.verr_contenido, name='verr_contenido'),
    path('compras/aumentarr_cantidad/<int:pk>/', views.aumentarr_cantidad, name='aumentarr_cantidad'),
    path('compras/disminuirr_cantidad/<int:pk>/', views.disminuirr_cantidad, name='disminuirr_cantidad'),
    path('compras/eliminar_detalle_compra/<int:pk>/eliminar/', views.eliminar_detalle_compra,
         name='eliminar_detalle_compra'),
]

