from django.contrib import admin

from inventario.models import Fabricacion
# Register your models here.
from inventario.models import Materia_Prima

admin.site.register(Materia_Prima)
admin.site.register(Fabricacion)
