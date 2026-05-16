from django.contrib import admin
from .models import Videojuego, Genero, Calificacion, Comentario


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'genero', 'fecha_creacion', 'media_calificacion']
    list_filter = ['genero', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion']


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['videojuego', 'usuario', 'puntuacion', 'fecha_creacion']
    list_filter = ['puntuacion']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'videojuego', 'fecha_creacion']
