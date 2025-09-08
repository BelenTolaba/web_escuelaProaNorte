from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .forms import RegistroForm, VerificacionVotanteForm, VotoForms
from .models import Votante, CustomUser


# ---------- REGISTRO ----------
def registro(request):
    if request.method == "POST":   
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():      
            try:
                user = form.save()
                messages.success(request, f"Registro exitoso para {user.nombre_completo}. Ahora puedes iniciar sesión.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Error al guardar el usuario: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = RegistroForm()    
    
    return render(request, "webproa/registro.html", {"form": form})


# ---------- LOGIN ----------
def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"¡Bienvenido {user.nombre_completo}!")
                return redirect("home")
            else:
                error = "Email o contraseña incorrectos"
        except CustomUser.DoesNotExist:
            error = "No existe una cuenta con ese email"
            
    return render(request, "webproa/login.html", {"error": error})


def logout_view(request):
    logout(request)   
    return redirect("home")


# ---------- PERFIL ----------
@login_required
def perfil(request):
    user = request.user
    datos_publicos = {
        "username": user.username,
        "nombre_completo": user.nombre_completo,
        "email": user.email,
        "curso": user.get_curso_display(),
        "foto_perfil": user.foto_perfil.url if user.foto_perfil else None
    }
    datos_privados = {"dni": user.dni}
    datos_admin = {"fecha_registro": user.date_joined}

    contexto = {
        "datos_publicos": datos_publicos,
        "datos_privados": datos_privados if request.user.is_staff or request.user == user else {},
        "datos_admin": datos_admin if request.user.is_staff else {},
    }
    return render(request, "webproa/perfil.html", contexto)


# ---------- VERIFICACIÓN PARA VOTAR ----------
@login_required
def verificacion_votante(request):
    user_dni = request.user.dni
    if Votante.objects.filter(dni=user_dni).exists():
        messages.info(request, "Ya has votado anteriormente. No puedes votar de nuevo.")
        return redirect("home")
    
    if request.method == "POST":
        form = VerificacionVotanteForm(request.POST)
        if form.is_valid():
            dni_ingresado = form.cleaned_data["dni"]
            if dni_ingresado != user_dni:
                messages.error(request, "El DNI ingresado no coincide con el de tu cuenta.")
                return render(request, "webproa/verificacion_votante.html", {"form": form})
            if not CustomUser.objects.filter(dni=dni_ingresado).exists():
                messages.error(request, "Error en la verificación. Contacta al administrador.")
                return render(request, "webproa/verificacion_votante.html", {"form": form})
            request.session['dni_verificado'] = dni_ingresado
            messages.success(request, "Verificación exitosa. Ahora puedes proceder a votar.")
            return redirect("votar")
    else:
        form = VerificacionVotanteForm()
    
    return render(request, "webproa/verificacion_votante.html", {"form": form})


# ---------- VOTAR ----------
@login_required
def votar(request):
    dni_verificado = request.session.get('dni_verificado')
    if not dni_verificado:
        messages.error(request, "Primero debes verificar tu identidad.")
        return redirect("verificacion_votante")
    
    if dni_verificado != request.user.dni:
        messages.error(request, "Error de sesión. Debes verificar tu identidad nuevamente.")
        del request.session['dni_verificado']
        return redirect("verificacion_votante")
    
    if Votante.objects.filter(dni=dni_verificado).exists():
        messages.info(request, "Ya has votado. No puedes votar de nuevo.")
        if 'dni_verificado' in request.session:
            del request.session['dni_verificado']
        return redirect("home")
    
    if request.method == "POST":
        form = VotoForms(request.POST)
        if form.is_valid():
            voto_seleccionado = form.cleaned_data.get("voto")
            if not voto_seleccionado:
                messages.error(request, "Debes seleccionar una lista para votar.")
                return render(request, "webproa/votar.html", {"form": form})
            user = request.user
            nombre_partes = user.nombre_completo.split()
            nombre = nombre_partes[0] if nombre_partes else ""
            apellido = " ".join(nombre_partes[1:]) if len(nombre_partes) > 1 else ""
            
            votante = Votante.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=dni_verificado,
                voto=voto_seleccionado
            )
            del request.session['dni_verificado']
            messages.success(request, "¡Tu voto se ha registrado correctamente!")
            return redirect("home")
        else:
            messages.error(request, "Error en el formulario. Por favor, selecciona una opción válida.")
    else:
        form = VotoForms()
    
    return render(request, "webproa/votar.html", {"form": form})


# ---------- RESETEAR (solo admin) ----------
@staff_member_required
def resetear_votaciones(request):
    count = Votante.objects.count()
    Votante.objects.all().delete()
    messages.success(request, f"Se han eliminado {count} votos y reiniciado las votaciones.")
    return redirect("home")


# ---------- OTRAS VIEWS ----------
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