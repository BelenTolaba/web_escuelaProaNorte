from django.db import models

class Votante(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido completo")
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")

    voto = models.CharField(
        max_length=50,
        choices=[
            ("grupo_azul", "Grupo Azul"),
            ("grupo_rojo", "Grupo Rojo"),
            ("grupo_verde", "Grupo Verde"),
        ],
        blank=True,
        null=True,
        verbose_name="Voto"
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "votantes"              
        ordering = ["nombre"]             
        verbose_name = "Votante"
        verbose_name_plural = "Votantes"

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"
    










from django.contrib.auth.models import AbstractUser

CURSOS = [
    (1, "1° Año"),
    (2, "2° Año"),
    (3, "3° Año"),
    (4, "4° Año"),
    (5, "5° Año"),
    (6, "6° Año"),
]

class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True
        )
    dni = models.CharField(
        max_length=8, 
        unique=True
        )
    curso = models.IntegerField(
        choices=CURSOS,
        default=1
        )
    foto_perfil = models.ImageField(
        upload_to="fotos_perfil/",
        blank=True,
        null=True
        )
    nombre_completo = models.CharField(
        max_length=100,
        blank=True
        )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "dni", "curso"]

    def avanzar_o_repetir(self, paso=True):
        """Si pasa de año suma +1, si repite queda igual. Si pasa del 6°, se borra."""
        if paso:
            if self.curso < 6:
                self.curso += 1
                self.save()
            else:
                self.delete()
        else:
            self.save()
