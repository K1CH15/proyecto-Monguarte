from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel

from productos.models import Producto
from usuario.models import Persona, Comision


# Módulo de venta
# Create your models here.
# Modelo de Venta

class Venta(SafeDeleteModel):
    fecha = models.DateTimeField(verbose_name="Fecha", default=timezone.now)

    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTICO = '0', _("Inactivo")

    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.ACTIVO, verbose_name="Estado")
    persona_vendedor = models.ForeignKey(Persona, verbose_name=_("Vendedor"), on_delete=models.CASCADE,
                                         related_name="ventas_vendedor")
    persona_cliente = models.ForeignKey(Persona, verbose_name=_("Cliente"), on_delete=models.CASCADE,
                                        related_name="ventas_cliente")

    def __str__(self):
        return "%s %s" % (self.persona_vendedor, self.persona_cliente)

    class meta:
        verbose_name_plural = "Venta"


# Modelo de Detalle Venta
from django.db import models


class Detalle_Venta(models.Model):
    cantidad_total = models.PositiveIntegerField(verbose_name="Cantidad Total", default=0)
    producto = models.ForeignKey(Producto, verbose_name=_("Producto"), on_delete=models.CASCADE,
                                 related_name="detalles_venta_producto")
    venta = models.ForeignKey(Venta, verbose_name=_("Venta"), on_delete=models.CASCADE, related_name="detalles_venta")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total",
                                      editable=False)

    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTIVO = '0', _("Inactivo")

    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.ACTIVO, verbose_name="Estado")

    def precio_unitario(self):
        return self.producto.precio_unitario

    def precio_unitario_formato_colombiano(self):
        return '${:,.0f}'.format(self.precio_unitario()).replace(',', '.')

    def valor_total_formato_colombiano(self):
        return '${:,.0f}'.format(self.valor_total).replace(',', '.')

    def __str__(self):
        return "%s %s %s" % (self.cantidad_total, self.precio_unitario(), self.venta)

    def save(self, *args, **kwargs):
        self.valor_total = self.precio_unitario() * self.cantidad_total

        super(Detalle_Venta, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Detalles Venta"
