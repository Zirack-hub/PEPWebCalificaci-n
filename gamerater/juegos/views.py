from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Videojuego, Calificacion, Comentario
from .forms import VideojuegoForm, CalificacionForm, ComentarioForm


class VideojuegoListView(ListView):
    """Muestra el catálogo completo de videojuegos con búsqueda."""
    model = Videojuego
    template_name = 'juegos/lista.html'
    context_object_name = 'juegos'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) | Q(descripcion__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busqueda'] = self.request.GET.get('q', '')
        return context


class VideojuegoDetailView(DetailView):
    """Muestra el detalle de un videojuego con calificaciones y comentarios."""
    model = Videojuego
    template_name = 'juegos/detalle.html'
    context_object_name = 'juego'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = self.get_object()

        # Formularios para calificación y comentario
        context['form_calificacion'] = CalificacionForm()
        context['form_comentario'] = ComentarioForm()
        context['calificaciones'] = juego.calificaciones.select_related('usuario')
        context['comentarios'] = juego.comentarios.select_related('autor')

        # Comprobar si el usuario ya calificó este juego
        if self.request.user.is_authenticated:
            context['ya_califico'] = juego.calificaciones.filter(
                usuario=self.request.user
            ).exists()
        else:
            context['ya_califico'] = False

        return context

    def post(self, request, *args, **kwargs):
        """Procesa el envío de calificaciones y comentarios desde la vista detalle."""
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para participar.')
            return redirect('usuarios:login')

        juego = self.get_object()
        accion = request.POST.get('accion')

        if accion == 'calificar':
            # Comprobar que no ha calificado ya
            if juego.calificaciones.filter(usuario=request.user).exists():
                messages.warning(request, 'Ya has calificado este juego.')
                return redirect('juegos:detalle', pk=juego.pk)

            form = CalificacionForm(request.POST)
            if form.is_valid():
                calificacion = form.save(commit=False)
                calificacion.videojuego = juego
                calificacion.usuario = request.user
                calificacion.save()
                messages.success(request, '¡Calificación enviada correctamente!')
            else:
                messages.error(request, 'Error en el formulario de calificación.')

        elif accion == 'comentar':
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.videojuego = juego
                comentario.autor = request.user
                comentario.save()
                messages.success(request, 'Comentario añadido.')
            else:
                messages.error(request, 'Error en el formulario de comentario.')

        return redirect('juegos:detalle', pk=juego.pk)


class VideojuegoCreateView(LoginRequiredMixin, CreateView):
    """Formulario para añadir un nuevo videojuego."""
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'juegos/formulario.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, '¡Videojuego añadido correctamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Añadir videojuego'
        context['boton_texto'] = 'Añadir'
        return context


class VideojuegoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Formulario para editar un videojuego existente."""
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'juegos/formulario.html'

    def test_func(self):
        """Solo el autor o staff puede editar."""
        juego = self.get_object()
        return self.request.user == juego.autor or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar este videojuego.')
        return redirect('juegos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Videojuego actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f'Editar: {self.get_object().titulo}'
        context['boton_texto'] = 'Guardar cambios'
        return context


class VideojuegoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Confirmación y borrado de un videojuego."""
    model = Videojuego
    template_name = 'juegos/confirmar_borrado.html'
    success_url = reverse_lazy('juegos:lista')
    context_object_name = 'juego'

    def test_func(self):
        juego = self.get_object()
        return self.request.user == juego.autor or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para eliminar este videojuego.')
        return redirect('juegos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Videojuego eliminado.')
        return super().form_valid(form)


def borrar_calificacion(request, pk):
    """Elimina la propia calificación del usuario en un juego."""
    calificacion = get_object_or_404(Calificacion, pk=pk)
    juego_pk = calificacion.videojuego.pk

    if request.user == calificacion.usuario or request.user.is_staff:
        calificacion.delete()
        messages.success(request, 'Calificación eliminada.')
    else:
        messages.error(request, 'No puedes eliminar esta calificación.')

    return redirect('juegos:detalle', pk=juego_pk)


def borrar_comentario(request, pk):
    """Elimina un comentario propio."""
    comentario = get_object_or_404(Comentario, pk=pk)
    juego_pk = comentario.videojuego.pk

    if request.user == comentario.autor or request.user.is_staff:
        comentario.delete()
        messages.success(request, 'Comentario eliminado.')
    else:
        messages.error(request, 'No puedes eliminar este comentario.')

    return redirect('juegos:detalle', pk=juego_pk)
