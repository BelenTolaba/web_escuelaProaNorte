from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistroForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .models import Votante
from django.contrib import messages
from .forms import VotanteForm, VotoForms

from django.contrib.auth.decorators import login_required

# signin/signup

def registro(request):
    if request.method == "POST":   
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():      
            form.save()        
            return redirect("login") 
    else:
        form = RegistroForm()    
    
    return render(request, "webproa/registro.html", {"form": form})




def login_view(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)  # Usamos email
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Email o contraseña incorrectos"

    return render(request, "webproa/login.html", {"error": error})

def logout_view(request):
    logout(request)   
    return redirect("home")


@login_required
def perfil(request):
    user = request.user
    # Datos visibles para todos
    datos_publicos = {
        "username": user.username,
        "nombre_completo": user.nombre_completo,
        "email": user.email,
        "curso": user.get_curso_display(),
        "foto_perfil": user.foto_perfil.url if user.foto_perfil else None
    }

    # Datos visibles solo para el usuario y admin
    datos_privados = {
        "dni": user.dni,
    }

    # Datos visibles solo para admin
    datos_admin = {
        "fecha_registro": user.date_joined,
    }

    contexto = {
        "datos_publicos": datos_publicos,
        "datos_privados": datos_privados if request.user.is_staff or request.user == user else {},
        "datos_admin": datos_admin if request.user.is_staff else {},
    }

    return render(request, "webproa/perfil.html", contexto)





# Votaciones


def registrar_votante(request):
    if request.method == "POST":
        form = VotanteForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]

            # Verificar si ya existe
            votante = Votante.objects.filter(dni=dni).first()
            if votante:
                messages.info(request, "Ya estabas registrado. Ahora podés votar.")
            else:
                votante = form.save()
                messages.success(request, "Registro exitoso. Ahora podés votar.")

            # Redirigir al formulario de votación sin pasar DNI por URL
            return redirect("votar")
    else:
        form = VotanteForm()

    return render(request, "webproa/registrar_votante.html", {"form": form})


@login_required
def votar(request):
    user = request.user

    votante = Votante.objects.filter(dni=user.dni).first()
    if not votante:
        messages.error(request, "No estás registrado como votante.")
        return redirect("registrar_votante")

    if votante.voto:
        messages.info(request, "Ya ingresaste tu voto. No puedes volver a votar hasta nuevo aviso.")
        return redirect("home")

    if request.method == "POST":
        form = VotoForms(request.POST, instance=votante)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu voto se ha registrado!")
            return redirect("home")
    else:
        form = VotoForms(instance=votante)

    return render(request, "webproa/votar.html", {"votante": votante, "form": form})








from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def resetear_votaciones(request):
    Votante.objects.update(voto=None)
    messages.success(request, "Se han reiniciado las votaciones.")
    return redirect("home")



# sitios


def home(request):
    return render(request, "webproa/home.html") 

def contactos(request):
    return render(request, "webproa/contactos.html") 

def votaciones(request):
    return render(request, "webproa/votaciones.html")

def novedades(request):
    return render(request, "webproa/novedades.html")

def informacion(request):
    return render(request, "webproa/informacion.html")
