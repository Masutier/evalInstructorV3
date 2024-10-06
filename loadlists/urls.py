from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('loadActivation', loadActivation, name='loadActivation'),
    path('activation', activation, name='activation'),

    path('loadings', loadings, name='loadings'),
    path('loadInstructores', loadInstructores, name='loadInstructores'),
    path('loadAprendicesMany', loadAprendicesMany, name='loadAprendicesMany'),

    path('uploadPhoto', uploadPhoto, name='uploadPhoto'),

]
