from django import forms
from django.forms import ModelForm
from django_select2.forms import Select2Widget

from venta.models import Detalle_Venta, Venta, Persona


class Detalle_VentaForm(ModelForm):
    class Meta:
        model = Detalle_Venta
        fields = '__all__'
        exclude = ["venta", "estado"]


class Detalle_VentaUpdateForm(ModelForm):
    class Meta:
        model = Detalle_Venta
        fields = '__all__'
        exclude = ["estado"]


class VentaForm(ModelForm):
    # Modifica el campo persona_vendedor para utilizar el widget Select2
    persona_vendedor = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    # Modifica el campo persona_cliente para utilizar el widget Select2
    persona_cliente = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )

    class Meta:
        model = Venta
        fields = '__all__'
        exclude = ["estado", "fecha"]


class VentaUpdateForm(ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        exclude = ["estado"]
