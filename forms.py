from django import forms
from .models import Votante, CustomUser
from django.contrib.auth.forms import UserCreationForm


class VerificacionVotanteForm(forms.Form):
    """
    Formulario simple para verificar identidad antes de votar.
    Solo necesita el DNI como verificación.
    """
    dni = forms.CharField(
        max_length=8,
        required=True,
        label="Tu DNI",
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Ingresa tu DNI para verificar tu identidad",
            "autocomplete": "off"
        })
    )


CANDIDATOS = [
    ("grupo_azul", "Grupo Azul"),
    ("grupo_rojo", "Grupo Rojo"),
    ("grupo_verde", "Grupo Verde"),
]

class VotoForms(forms.Form):
    """
    Formulario para votar. No hereda de ModelForm porque no queremos
    que se guarde automáticamente sin voto.
    """
    voto = forms.ChoiceField(
        choices=CANDIDATOS,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Elige tu grupo favorito",
        required=True,
        error_messages={'required': 'Debes seleccionar una opción para votar.'}
    )


class RegistroForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=100,
        required=True,
        label="Nombre completo",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre y apellido completo"})
    )
    email = forms.EmailField(
        required=True,
        label="Email institucional",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "tu-nombre@escuelasproa.edu.ar"})
    )
    dni = forms.CharField(
        max_length=8,
        required=True,
        label="DNI",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu número de DNI"})
    )
    curso = forms.ChoiceField(
        label="Curso actual",
        choices=CustomUser._meta.get_field("curso").choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    foto_perfil = forms.ImageField(
        required=False,
        label="Foto de perfil (opcional)",
        widget=forms.FileInput(attrs={"class": "form-control"})
    )
    
    # Personalizar campos de contraseña
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ingresa tu contraseña"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirma tu contraseña"})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "nombre_completo", "email", "dni", "curso", "foto_perfil", "password1", "password2"]
        
    def clean_email(self):
        """Validar que el email sea del dominio institucional"""
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@escuelasproa.edu.ar'):
            raise forms.ValidationError(
                'Solo se aceptan emails institucionales con dominio @escuelasproa.edu.ar'
            )
        return email
        
    def save(self, commit=True):
        """Sobrescribir save para asegurar que se guarde correctamente"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nombre_completo = self.cleaned_data['nombre_completo']
        user.dni = self.cleaned_data['dni']
        user.curso = self.cleaned_data['curso']
        
        if commit:
            user.save()
            # Guardar la foto después si existe
            if self.cleaned_data.get('foto_perfil'):
                user.foto_perfil = self.cleaned_data['foto_perfil']
                user.save()
        return user
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el campo username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario único'
        })


# ✅ ELIMINAMOS VotanteForm porque ya no la necesitamos
# El registro de votantes se hace automáticamente al votar