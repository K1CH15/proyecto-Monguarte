from django.contrib.auth.models import User, Group
from django.core.validators import integer_validator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel


# Módulo de usuarios
# Create your models here.
# Modelo Persona
# def letras_uniquemente(value):
#     if not value.isalpha():
#         raise ValidationError("El campo solo permite letras.")
class Persona(SafeDeleteModel):
    class TipoDocumento(models.TextChoices):
        CC = 'CC ', _("Cédula de Ciudadanía")
        TI = 'TI', _("Tarjeta de Identidad")
        CE = 'CE', _("Cédula de Extranjería")

    tipo_documento = models.CharField(max_length=3, choices=TipoDocumento.choices, default=TipoDocumento.CC,
                                      verbose_name="Tipo de Documento")
    numero_documento = models.CharField(max_length=10, validators=[integer_validator, RegexValidator(r'^\d+$',
                                                                                                     message="Este campo solo permite valores numericos")],
                                        verbose_name="Número de Documento", unique=True)
    nombres = models.CharField(max_length=30, verbose_name="Nombres")
    apellidos = models.CharField(max_length=30, verbose_name="Apellidos")
    telefono = models.CharField(max_length=10,
                                validators=[integer_validator, MaxLengthValidator(10), RegexValidator(r'^\d+$')],
                                verbose_name="Número Telefónico", unique=True)
    correo_electronico = models.EmailField(max_length=50, verbose_name="Correo Electrónico", unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios', null=True, blank=True)
    rol = models.ForeignKey(Group, verbose_name="Rol", on_delete=models.SET_NULL, null=True, blank=True,
                            help_text="Roles:Administrador,Vendedor,")

    class Estado(models.TextChoices):
        ACTIVO = '1', _("Activo")
        INACTICO = '0', _("Inactivo")

    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.ACTIVO, verbose_name="Estado")
    ips = models.CharField(max_length=10, verbose_name="IPS", blank=True, null=True)

    def __str__(self):
        return "%s %s %s %s %s %s" % (
            "Numero De Documento:", self.numero_documento, self.nombres, self.apellidos, ",Rol:", self.rol)

    class meta:
        verbose_name_plural = "Persona"


# Modelo de Comisión
class Comision(models.Model):
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    valor_comision = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor de Comisión")

    @classmethod
    def get_or_create_total_comision(cls):
        total_comision, created = cls.objects.get_or_create(pk=1)
        return total_comision

    @classmethod
    def accumulate_comision(cls, comision_valor):
        total_comision = cls.get_or_create_total_comision()
        total_comision.valor_comision += comision_valor
        total_comision.save()

    def valor_comision_formato_colombiano(self):
        return '${:,.0f}'.format(self.valor_comision).replace(',', '.')

