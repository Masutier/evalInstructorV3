from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('obtener_datos_aprendiz/<pk>', obtener_datos_aprendiz, name='obtener_datos_aprendiz'),
    path('obtener_preguntas/<pk>/<pk2>', obtener_preguntas, name='obtener_preguntas'),
    path('guardar_respuestas/<pk>/<pk2>', guardar_respuestas, name='guardar_respuestas'),

]
