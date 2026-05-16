from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse


class Genero(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'géneros'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videojuegos')
    genero = models.ForeignKey(
        Genero, on_delete=models.SET_NULL, null=True, blank=True, related_name='videojuegos'
    )

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('juegos:detalle', kwargs={'pk': self.pk})

    def media_calificacion(self):
        """Devuelve la media de puntuaciones o None si no hay calificaciones."""
        resultado = self.calificaciones.aggregate(Avg('puntuacion'))
        media = resultado['puntuacion__avg']
        return round(media, 1) if media is not None else None

    def num_calificaciones(self):
        return self.calificaciones.count()


class Calificacion(models.Model):
    PUNTUACIONES = [(i, str(i)) for i in range(1, 11)]

    puntuacion = models.IntegerField(choices=PUNTUACIONES)
    resena = models.TextField(verbose_name='Reseña')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    videojuego = models.ForeignKey(
        Videojuego, on_delete=models.CASCADE, related_name='calificaciones'
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')

    class Meta:
        # Un usuario solo puede calificar una vez cada juego
        unique_together = ('videojuego', 'usuario')
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} → {self.videojuego.titulo}: {self.puntuacion}/10"


class Comentario(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    videojuego = models.ForeignKey(
        Videojuego, on_delete=models.CASCADE, related_name='comentarios'
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.autor.username} en '{self.videojuego.titulo}'"
