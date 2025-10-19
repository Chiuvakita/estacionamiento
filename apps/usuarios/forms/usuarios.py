from django import forms
from ..models import Usuario

class UsuarioForm(forms.ModelForm):

    ROL_CHOICES = [
        ('', 'Seleccione un rol'),
        ('Cliente', 'Cliente'),
        ('Empleado', 'Empleado'),
        ('Administrador', 'Administrador'),
    ]
    
    rut = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'min': 1,
            'max': 999999999,
            'class': 'form-control'
        }),
        help_text='Ingrese el RUT sin puntos ni guión'
    )
    
    nombre = forms.CharField(
        max_length=45,
        widget=forms.TextInput(attrs={
            'minlength': 2,
            'pattern': '[A-Za-zÁÉÍÓÚáéíóúÑñ\\s]+',
            'title': 'Solo se permiten letras y espacios',
            'class': 'form-control'
        })
    )
    
    apellidoPaterno = forms.CharField(
        max_length=45,
        label='Apellido Paterno',
        widget=forms.TextInput(attrs={
            'minlength': 2,
            'pattern': '[A-Za-zÁÉÍÓÚáéíóúÑñ]+',
            'title': 'Solo se permiten letras',
            'class': 'form-control'
        })
    )
    
    apellidoMaterno = forms.CharField(
        max_length=45,
        label='Apellido Materno',
        widget=forms.TextInput(attrs={
            'minlength': 2,
            'pattern': '[A-Za-zÁÉÍÓÚáéíóúÑñ]+',
            'title': 'Solo se permiten letras',
            'class': 'form-control'
        })
    )
    
    numeroTelefono = forms.CharField(
        max_length=45,
        label='Número de Teléfono',
        widget=forms.TextInput(attrs={
            'pattern': '[0-9]{8,12}',
            'title': 'Ingrese un número de teléfono válido (8-12 dígitos)',
            'placeholder': 'Ej: 987654321',
            'class': 'form-control'
        })
    )
    
    rol = forms.ChoiceField(
        choices=ROL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    discapacidad = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Marque si el usuario tiene alguna discapacidad'
    )
    
    clave = forms.CharField(
        max_length=130,
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'minlength': 6,
            'placeholder': 'Ingrese la contraseña',
            'class': 'form-control'
        }),
        help_text='Contraseña de al menos 6 caracteres'
    )
    
    confirmar_clave = forms.CharField(
        max_length=130,
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'minlength': 6,
            'placeholder': 'Confirme la contraseña',
            'class': 'form-control'
        }),
        help_text='Repita la contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'numeroTelefono', 'rol', 'discapacidad', 'clave']
    
    def __init__(self, *args, **kwargs):
        rutReadonly = kwargs.pop('rutReadonly', False)
        super().__init__(*args, **kwargs)
        
        if rutReadonly:
            self.fields['rut'].widget.attrs['readonly'] = True
            self.fields['rut'].widget.attrs.update({'class': 'form-control readonly-field'})
    
    def clean_rut(self):
        rutData = self.cleaned_data.get('rut')
        if rutData and (rutData < 1000000 or rutData > 999999999):
            raise forms.ValidationError('El RUT debe tener entre 7 y 9 dígitos')
        return rutData
    
    def clean_nombre(self):
        nombreData = self.cleaned_data.get('nombre')
        if nombreData and len(nombreData.strip()) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres')
        return nombreData.strip().title()
    
    def clean_apellidoPaterno(self):
        apellidoData = self.cleaned_data.get('apellidoPaterno')
        if apellidoData and len(apellidoData.strip()) < 2:
            raise forms.ValidationError('El apellido paterno debe tener al menos 2 caracteres')
        return apellidoData.strip().title()
    
    def clean_apellidoMaterno(self):
        apellidoData = self.cleaned_data.get('apellidoMaterno')
        if apellidoData and len(apellidoData.strip()) < 2:
            raise forms.ValidationError('El apellido materno debe tener al menos 2 caracteres')
        return apellidoData.strip().title()
    
    def clean_clave(self):
        claveData = self.cleaned_data.get('clave')
        if claveData and len(claveData) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres')
        return claveData
    
    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get('clave')
        confirmar_clave = cleaned_data.get('confirmar_clave')
        
        if clave and confirmar_clave:
            if clave != confirmar_clave:
                raise forms.ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data