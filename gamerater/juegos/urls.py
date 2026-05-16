from django.urls import path
from . import views

app_name = 'juegos'

urlpatterns = [
    # Catálogo y detalle
    path('', views.VideojuegoListView.as_view(), name='lista'),
    path('<int:pk>/', views.VideojuegoDetailView.as_view(), name='detalle'),

    # CRUD
    path('nuevo/', views.VideojuegoCreateView.as_view(), name='crear'),
    path('<int:pk>/editar/', views.VideojuegoUpdateView.as_view(), name='editar'),
    path('<int:pk>/borrar/', views.VideojuegoDeleteView.as_view(), name='borrar'),

    # Calificaciones y comentarios
    path('calificacion/<int:pk>/borrar/', views.borrar_calificacion, name='borrar_calificacion'),
    path('comentario/<int:pk>/borrar/', views.borrar_comentario, name='borrar_comentario'),
]
