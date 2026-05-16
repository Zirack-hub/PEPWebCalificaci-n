from django import forms
from .models import Videojuego, Calificacion, Comentario


class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'descripcion', 'imagen', 'genero']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del videojuego'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del juego...'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
        }


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['puntuacion', 'resena']
        widgets = {
            'puntuacion': forms.Select(attrs={'class': 'form-select'}),
            'resena': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu reseña...'}),
        }
        labels = {
            'puntuacion': 'Puntuación (1-10)',
            'resena': 'Reseña',
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Deja un comentario...'}),
        }
        labels = {
            'texto': '',
        }


class BusquedaForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar videojuegos...',
        })
    )
