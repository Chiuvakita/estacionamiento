from django import forms
from apps.empresas.models import Empresa, Sucursal

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

# Definir formulario para Sucursal
class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        exclude = ['empresa'] #Como empresa es una clave foranea, no se muestra en el formulario
        fields = '__all__'