from django.contrib import admin
from django import forms
from .models import Usuario
from django.contrib.auth.models import User
class UsuarioAdminForm(forms.ModelForm):
    clave_nueva = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        required=False,
        help_text='Dejar en blanco si no deseas cambiar la contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = '__all__'

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm 
    
    list_display = ('rut', 'nombre', 'apellidoPaterno', 'rol', 'numeroTelefono', 'discapacidad')
    list_filter = ('rol', 'discapacidad')
    search_fields = ('rut', 'nombre', 'apellidoPaterno', 'apellidoMaterno')
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('rut', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'numeroTelefono')
        }),
        ('Autenticación y Permisos', {
            'fields': ('clave_nueva', 'rol', 'discapacidad')
        }),
    )
    
    def save_model(self, obj, form, change):
        clave_nueva = form.cleaned_data.get('clave_nueva')
        
        if not change and not clave_nueva:
            obj.setClave('temporal')
        elif clave_nueva:
            obj.setClave(clave_nueva)
        
        obj.save()
        

        try:
            user = User.objects.get(username=str(obj.rut))
            if clave_nueva:
                user.set_password(clave_nueva)
                user.save()
        except User.DoesNotExist:
            if clave_nueva:
                User.objects.create_user(username=str(obj.rut), password=clave_nueva)
            else:
                User.objects.create_user(username=str(obj.rut), password='temporal')