from django.urls import path
from . import views





urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path('registrar/', views.registrar_votante, name='registrar_votante'),
    path('votar/<str:dni>/', views.votar, name='votar'),

    path("home", views.home, name="home"),
    path("contactos", views.contactos, name="contactos"),
    path("votaciones", views.votaciones, name="votaciones"),
    path("novedades", views.novedades, name="novedades"),
    path("informacion", views.informacion, name="informacion"),
] 