"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from accounts import views
from base.views import (
    principal,
    logout_user,
    usuario_vista,
    compra_vista,
    inventario_vista,
    venta_vista,
    producto_vista,
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path("inicio/", principal, name="index"),
    path('', auth_views.LoginView.as_view(), name='inicio'),
    path('reiniciar/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reiniciar/enviar', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reiniciar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reiniciar/completo', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', logout_user, name="logout"),

    path('usuarios/', include('usuario.urls')),
    path('compras/', include('compra.urls')),
    path('inventarios/', include('inventario.urls')),
    path('ventas/', include('venta.urls')),
    path('productos/', include('productos.urls')),
    # vistas de modulos
    path('Usuarios/', usuario_vista, name="usuario"),
    path('Compras/', compra_vista, name="compras"),
    path('Inventarios/', inventario_vista, name="inventario"),
    path('Ventas/', venta_vista, name="venta"),
    path('Productos/', producto_vista, name="producto"),
    path('inicio/abrir-pdf/', TemplateView.as_view(template_name='partials/archivo_pdf.html'), name='abrir_pdf'),

    path('templates/partials/', include('accounts.urls')),
    path('Registro Usuario', views.register, name='Registrarse'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),

]
