from django import forms
from .models import Votante

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


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Usa un email válido"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
