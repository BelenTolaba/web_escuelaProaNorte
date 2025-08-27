from django import forms
from .models import Votante, CustomUser   # Importar CustomUser en lugar de User
from django.contrib.auth.forms import UserCreationForm


class VotanteForm(forms.ModelForm):
    class Meta:
        model = Votante
        fields = ["nombre", "apellido", "dni"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            "apellido": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido completo"}),
            "dni": forms.TextInput(attrs={"class": "form-control", "placeholder": "DNI único"}),
        }


CANDIDATOS = [
    ("grupo_azul", "Grupo Azul - Propuesta: Más deportes y actividades artísticas"),
    ("grupo_rojo", "Grupo Rojo - Propuesta: Mejorar biblioteca y tecnología"),
    ("grupo_verde", "Grupo Verde - Propuesta: Jornadas de medio ambiente"),
]

class VotoForms(forms.ModelForm):
    voto = forms.ChoiceField(
        choices=CANDIDATOS,
        widget=forms.RadioSelect,
        label="Elige tu grupo"
    )

    class Meta:
        model = Votante
        fields = ["voto"]



class RegistroForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=100,
        required=True,
        label="Nombre completo",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre y apellido"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    dni = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "DNI"})
    )
    curso = forms.ChoiceField(
        choices=CustomUser._meta.get_field("curso").choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "nombre_completo", "email", "dni", "curso", "foto_perfil", "password1", "password2"]