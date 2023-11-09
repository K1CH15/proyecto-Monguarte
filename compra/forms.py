from django import forms
from django.forms import ModelForm
from compra.models import Compra,Detalle_Compra,Persona,Materia_Prima
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_select2.forms import Select2Widget

class CompraForm(ModelForm):
    # Modifica el campo persona para utilizar el widget Select2
    persona_admin = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    # Modifica el campo persona para utilizar el widget Select2
    persona_proveedor = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    class Meta:
        model = Compra
        fields = "__all__"
        exclude = ["estado"]
        success_message = 'la compra se añadió correctamente'

class CompraUpdateForm(ModelForm):
    class Meta:
        model = Compra
        fields ="__all__"
        exclude=["id","fecha"]
        success_message = 'la compra se actualizó correctamente'

class Detalle_CompraForm(ModelForm):
        # Modifica el campo materia_prima para utilizar el widget Select2
    materia_prima = forms.ModelChoiceField(
        queryset=Materia_Prima.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    class Meta:
        model = Detalle_Compra
        fields = "__all__"
        exclude = ["compra","estado"]
        success_message = 'el detalle de la compra se añadió correctamente'


class Detalle_CompraUpdateForm(ModelForm):

    class Meta:
        model = Detalle_Compra
        fields = "__all__"
        exclude =["id","estado"]
        success_message = 'el detalle de la compra se actualizó correctamente'

