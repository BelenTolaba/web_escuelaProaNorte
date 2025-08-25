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