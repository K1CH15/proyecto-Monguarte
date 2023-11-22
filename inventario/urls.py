from django.urls import path

from inventario.views import fabricacion_listar, fabricacion_crear, fabricacion_modificar, fabricacion_eliminar, \
    fabricacion_detalle_listar, fabricacion_detalle_finalizar
from inventario.views import materia_prima_crear, materia_prima_eliminar, materia_prima_listar, materia_prima_modificar
from . import views

urlpatterns = [

    path('materia prima/', materia_prima_listar, name="materias-primas"),
    path('materia prima/crear/', materia_prima_crear, name="materias-primas-crear"),
    path('materia prima/modificar/<int:pk>/', materia_prima_modificar, name="materias-primas-modificar"),
    path('materia prima/eliminar/<int:pk>/', materia_prima_eliminar, name="materias-primas-eliminar"),

    path('fabricacion/', fabricacion_listar, name="fabricaciones"),
    path('fabricacion_detalle/<int:pk>/', fabricacion_detalle_listar, name="fabricacion_detalle"),
    path('fabricacion/crear/', fabricacion_crear, name="fabricaciones-crear"),
    path('fabricacion/modificar/<int:pk>/', fabricacion_modificar, name="fabricaciones-modificar"),
    path('fabricacion/eliminar/<int:pk>/', fabricacion_eliminar, name="fabricaciones-eliminar"),
    path('finalizar/<int:pk>/', fabricacion_detalle_finalizar, name='fabricacion-finalizar'),
    path('verr_contenido/<int:pk>/', views.verr_contenido, name='verr_contenido'),
    path('fabricacion/aumentarr_cantidad/<int:pk>/', views.aumentarr_cantidad, name='aumentarr_cantidad'),
    path('fabricacion/disminuirr_cantidad/<int:pk>/', views.disminuirr_cantidad, name='disminuirr_cantidad'),
    path('fabricacion/eliminar_fabricacion_detalle/<int:pk>/eliminar/', views.eliminarr_fabricacion_detalle,
         name='eliminar_fabricacion_detalle'),
    # path('stock/', listar_stock, name='stock'),
    # path('stock/agregar/', agregar_stock, name='agregar_stock'),

]
