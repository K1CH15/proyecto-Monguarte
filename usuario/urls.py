from django.urls import path

from usuario.views import comision_crear, comision_listar, comision_modificar
from usuario.views import persona_crear, persona_listar, persona_modificar, persona_eliminar

urlpatterns = [
    path('persona/', persona_listar, name="personas"),
    path('persona/crear/', persona_crear, name="personas-crear"),
    path('persona/modificar/<int:pk>/', persona_modificar, name="personas-modificar"),
    path('persona/eliminar/<int:pk>/', persona_eliminar, name="personas-eliminar"),

    path('comisión/', comision_listar, name="comisiones"),
    path('comisión/crear/', comision_crear, name="comisiones-crear"),
    path('comisión/modificar/<int:pk>/', comision_modificar, name="comisiones-modificar"),

    # path('contabilidad/eliminar/<int:pk>/', contabilidad_eliminar , name="contabilidades-eliminar" ),
    #
    # path('aporte/', aporte_listar , name="aportes"),
    # path('aporte/crear/', aporte_crear , name="aportes-crear" ),
    # path('aporte/modificar/<int:pk>/', aporte_modificar , name="aportes-modificar" ),
    # path('aporte/eliminar/<int:pk>/', aporte_eliminar , name="aportes-eliminar" ),
    #
    # path('ips/',ips_listar , name="ipss"),
    # path('ips/crear/',ips_crear , name="ipss-crear" ),
    # path('ips/modificar/<int:pk>/', ips_modificar , name="ipss-modificar" ),
    # path('ips/eliminar/<int:pk>/',ips_eliminar , name="ipss-eliminar" ),
    #
    # path('nomina/',nomina_listar , name="nominas"),
    # path('nomina/crear/',nomina_crear , name="nominas-crear" ),
    # path('nomina/modificar/<int:pk>/',nomina_modificar , name="nominas-modificar" ),
    # path('nomina/eliminar/<int:pk>/',nomina_eliminar , name="nominas-eliminar" ),
    #
    # path('trabajador/',trabajador_listar , name="trabajadores"),
    # path('trabajador/crear/',trabajador_crear , name="trabajadores-crear" ),
    # path('trabajador/modificar/<int:pk>/', trabajador_modificar, name="trabajadores-modificar"),
    #

]
