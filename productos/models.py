from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from safedelete.models import SafeDeleteModel

class Producto(SafeDeleteModel):
    nombre=models.CharField(max_length=45,verbose_name="Nombre")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0, validators=[MaxValueValidator(9999999999)],
        null=True,
        blank=True)
    costo_fabricacion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                     verbose_name="Costo de Fabricación")

    def precio_formato_colombiano(self):
        return '${:,.0f}'.format(self.precio_unitario).replace(',', '.')
    cantidad=models.ForeignKey
    stock = models.PositiveIntegerField(default=0, editable=False, verbose_name="Stock de Materia Prima")

    class Estado(models.TextChoices):
        ACTIVO='1',_("Activo")
        INACTIVO='0',_("Inactivo")
    estado=models.CharField(max_length=1,choices=Estado.choices,default=Estado.ACTIVO,verbose_name="Estado")
    class Tamano(models.TextChoices):
        PEQUENO = '1',_("Pequeño")
        MEDIANO = '2',_("Mediano")
        GRANDE = '3',_("Grande")
    tamano=models.CharField(max_length=1,choices=Tamano.choices,verbose_name="Tamaño")
    class Tipo(models.TextChoices):
        TIPO1 = '1',_("Prenda de vestir")
        TIPO2 = '2',_("Accesorio")
        TIPO3 = '3',_("Figura")

    tipo=models.CharField(max_length=1,choices=Tipo.choices,verbose_name="Tipo")

    def __str__(self):
        return"%s %s %s %s %s %s"%("Producto de Nombre:",self.nombre,"de Tipo:",self.get_tipo_display(),"y Tamaño:",self.get_tamano_display())
    class meta:
        verbose_name_plural="Producto"