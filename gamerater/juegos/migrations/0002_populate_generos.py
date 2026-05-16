from django.db import migrations


GENEROS = [
    ("Acción",          "Juegos con combate rápido y reflejos como protagonistas."),
    ("Aventura",        "Juegos centrados en exploración e historia."),
    ("RPG",             "Juegos de rol con desarrollo de personaje y narrativa profunda."),
    ("Deportes",        "Simulaciones de deportes reales como fútbol, baloncesto o tenis."),
    ("Carreras",        "Juegos de conducción y competición de vehículos."),
    ("Estrategia",      "Juegos que requieren planificación y toma de decisiones."),
    ("Simulación",      "Juegos que replican situaciones o sistemas del mundo real."),
    ("Terror",          "Juegos de miedo y supervivencia con atmósfera opresiva."),
    ("Plataformas",     "Juegos de saltos y obstáculos por niveles."),
    ("Lucha",           "Juegos de combate uno contra uno o en equipo."),
    ("Shooter",         "Juegos de disparos en primera o tercera persona."),
    ("Puzzle",          "Juegos de lógica y resolución de enigmas."),
    ("Multijugador",    "Juegos diseñados para jugar en línea con otros usuarios."),
    ("Mundo abierto",   "Juegos con mapas grandes y libertad de exploración total."),
    ("Indie",           "Juegos desarrollados por estudios independientes."),
]


def insertar_generos(apps, schema_editor):
    Genero = apps.get_model('juegos', 'Genero')
    for nombre, descripcion in GENEROS:
        Genero.objects.create(nombre=nombre, descripcion=descripcion)


def eliminar_generos(apps, schema_editor):
    Genero = apps.get_model('juegos', 'Genero')
    Genero.objects.filter(nombre__in=[g[0] for g in GENEROS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('juegos', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(insertar_generos, eliminar_generos),
    ]