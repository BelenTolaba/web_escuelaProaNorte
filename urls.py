from django.urls import path
from . import views

urlpatterns = [
    # Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),

    # Autenticación
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Proceso de votación (2 pasos)
    path('verificacion/', views.verificacion_votante, name='verificacion_votante'),
    path('votar/', views.votar, name='votar'),

    # Administración (solo admin)
    path('resetear-votaciones/', views.resetear_votaciones, name='resetear_votaciones'),

    # Páginas principales
    path("home/", views.home, name="home"),
    path("contactos/", views.contactos, name="contactos"),
    path("votaciones/", views.votaciones, name="votaciones"),
    path("novedades/", views.novedades, name="novedades"),
    path("informacion/", views.informacion, name="informacion"),
    
    # Redirigir raíz a home
    path("", views.home, name="home"),
]