from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render 
from .forms import RegistroForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .models import Votante
from .forms import VotoForms
from django.contrib import messages
from .forms import VotanteForm, VotoForms

def registro(request):
    if request.method == "POST":   
        form = RegistroForm(request.POST)
        if form.is_valid():      
            user = form.save()        
            return redirect("login") 
    else:
        form = RegistroForm()    
    
    return render(request, "webproa/registro.html", {"form": form})




def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "webproa/login.html", {"form": form})

def logout_view(request):
    logout(request)   
    return redirect("login")







def registrar_votante(request):
    votante = None
    if request.method == "POST":
        form = VotanteForm(request.POST)
        if form.is_valid():
            try:
                votante = form.save()
                messages.success(request, "Se ha registrado correctamente")
                return redirect('votar', dni=votante.dni)
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = VotanteForm()

    return render(request, "webproa/registrar_votante.html", {"form": form, "votante": votante})

def votar(request, dni):
    votante = Votante.objects.get(dni=dni)

    if votante.voto:
        messages.info(request, "Ya has votado.")
        return redirect("gracias")

    if request.method == "POST":
        form = VotoForms(request.POST, instance=votante)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu voto se ha registrado!")
            return redirect("registrar_votante")
    else:
        form = VotoForms(instance=votante)

    return render(request, "webproa/votar.html", {"form": form, "votante": votante})





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
