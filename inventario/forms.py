from django import forms
from django.forms import ModelForm
from inventario.models import Materia_Prima,Producto,Fabricacion, Fabricacion_Detalle
from django_select2.forms import Select2Widget
class Materia_PrimaForm(ModelForm):

    class Meta:
        model = Materia_Prima
        fields = "__all__"
        exclude=["estado","stock","precio_unitario"]
class Materia_PrimaUptadeForm(ModelForm):

    class Meta:
        
        model = Materia_Prima
        fields = "__all__"
        exclude = ["estado", "stock","precio_unitario"]
class FabricacionForm(ModelForm):
            # Modifica el campo materia_prima para utilizar el widget Select2
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    class Meta:
        model = Fabricacion
        fields = "__all__"
        exclude = ['estado','materia_prima','cantidad_materia','costo_fabricacion']


class FabricacionUptadeForm(ModelForm):
    class Meta:
        model = Fabricacion
        fields = "__all__"
        exclude = ['estado', 'materia_prima', 'cantidad_materia','costo_fabricacion']

class Fabricacion_DetalleForm(ModelForm):
    materia_prima = forms.ModelChoiceField(
        queryset=Materia_Prima.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    class Meta:
        model = Fabricacion_Detalle
        fields = "__all__"
        exclude = ['fabricacion','estado']

class Fabricacion_DetalleUptadeForm(ModelForm):
    materia_prima = forms.ModelChoiceField(
        queryset=Materia_Prima.objects.all(),
        widget=Select2Widget,  # Utiliza el widget Select2
    )
    class Meta:
        model = Fabricacion_Detalle
        fields = "__all__"
        exclude = ['fabricacion', 'estado']
# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['materia_prima', 'cantidad', 'precio_unitario']
