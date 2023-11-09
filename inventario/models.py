from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from productos.models import Producto
from venta.models import Detalle_Venta
from django.core.validators import MaxValueValidator
from safedelete.models import SafeDeleteModel
from decimal import Decimal


class Materia_Prima(SafeDeleteModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de la Materia Prima",
                              help_text="Ingrese el Nombre de la Materia Prima")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MaxValueValidator(9999999999)],
                                          verbose_name="Precio Unitario", default=0, )

    class Unidad_Medida(models.TextChoices):
        GRAMO = '0', _("Gramos (gr) ")
        LIBRRA = '1', _("Libras (lb)")

    unidad_medida = models.CharField(max_length=1, choices=Unidad_Medida.choices,
                                     verbose_name=_("seleccione la unidad de medida"))

    class Tipos(models.TextChoices):
        CERA = '1', _("Cera")
        ESPARTO = '2', _("Esparto")
        LANA = '3', _("Lana")

    tipo = models.CharField(max_length=3, choices=Tipos.choices, verbose_name="seleccione el Tipo de Materia Prima", )
    color = models.CharField(max_length=20, verbose_name="Color Materia Prima")

    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTIVO = '0', _("Inactivo")

    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.ACTIVO, verbose_name="Estado")
    # si la materia prima ya exite con los datos iguales simplemete se suma falta para que se sume automaticamente
    # detalle_compra=models.ForeignKey(verbose_name=_("Cantidad"),help_text="Cantidad de Materia Prima",on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock de Materia Prima")

    def precio_unitario_formato_colombiano(self):
        return '${:,.0f}'.format(self.precio_unitario).replace(',', '.')

    def __str__(self):
        return "%s %s %s %s %s %s" % (
            "Nombre de la Materia Prima:", self.nombre, "de Tipo:", self.get_tipo_display(), "y de Color:", self.color)

    def clean(self):
        if self.stock != 0:
            raise ValidationError(
                "Una vez que el stock se haya actualizado a cero después de una compra, no se permitirán más modificaciones en la materia prima. ")

    class Meta:
        verbose_name_plural = "Materia Prima"


class Fabricacion(SafeDeleteModel):
    fecha = models.DateTimeField(verbose_name="Fecha de Fabricación", auto_now_add=True)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE)
    cantidad_producto = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0,
                                                    help_text="La cantidad tiene que ser menor a 100")
    costo_fabricacion = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                            verbose_name="Costo de Fabricación")

    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTIVO = '0', _("Inactivo")

    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.ACTIVO, verbose_name="Estado")

    def __str__(self):
        return "%s" % (self.cantidad_producto)


class Fabricacion_Detalle(SafeDeleteModel):
    cantidad_materia = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0,
                                                   help_text="cantidad utilizada para hacer el producto")
    materia_prima = models.ForeignKey(Materia_Prima, verbose_name="Materia Prima", on_delete=models.CASCADE)
    fabricacion = models.ForeignKey(Fabricacion, verbose_name="Fabricacion", on_delete=models.CASCADE)

    def calcular_costo_fabricacion(self):
        costo_fabricacion = Decimal(0)
        if self.materia_prima and self.cantidad_materia > 0:
            costo_fabricacion = self.materia_prima.precio_unitario * self.cantidad_materia
        return costo_fabricacion
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
# class Stock(SafeDeleteModel):
#     materia_prima = models.OneToOneField(Materia_Prima, on_delete=models.CASCADE)
#     cantidad = models.PositiveIntegerField(default=0, verbose_name="Stock de Materia Prima")
#     precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio Unitario")
#     valor_total_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total de la Compra")
#
#     def __str__(self):
#         return f"{self.materia_prima.nombre} - Stock: {self.cantidad} - Precio Unitario: {self.precio_unitario}"
#
#     class Meta:
#         verbose_name_plural = "Stocks de Materia Prima"
