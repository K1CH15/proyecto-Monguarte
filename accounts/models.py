from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel
from django.core.validators import integer_validator
from django.utils.translation import gettext_lazy as _
class Register(SafeDeleteModel):

    numero_documento = models.OneToOneField(User,max_length=10, validators=[integer_validator],verbose_name="Número de Documento",unique=True, on_delete=models.CASCADE,related_name="numero_documento_set")

    activo = models.BooleanField(default=False)
    class TipoDocumento(models.TextChoices):
        CC='CC ',_("Cédula de Ciudadanía")
        TI='TI',_("Tarjeta de Identidad")
        CE='CE',_("Cédula de Extranjería")
    tipo_documento=models.OneToOneField(User,max_length=3,choices=TipoDocumento.choices,default=TipoDocumento.CC,verbose_name="Tipo de Documento",on_delete=models.CASCADE,related_name="tipo_documento_set")


    # def clean(self):
    #     self.correo = self.correo.title()
    #     self.usuario = self.usuario.title()
    #     self.contrasena = self.contrasena.lower()
    #
    # def __str__(self):
    #     return "%s %s" % (self.correo, self.usuario)

    class Meta:
        verbose_name_plural = "Registers"
