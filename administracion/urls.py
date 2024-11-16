from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('administracion', administracion, name='administracion'),
    path('createFinalReportFicha', createFinalReportFicha, name='createFinalReportFicha'),
    path('createFinalReportDocumento', createFinalReportDocumento, name='createFinalReportDocumento'),
    path('fullTableFichaInstructor', fullTableFichaInstructor, name='fullTableFichaInstructor'),
    path('fullTableDocInstructor', fullTableDocInstructor, name='fullTableDocInstructor'),
    path('userLogin', userLogin, name='userLogin'),
    path('userLogout', userLogout, name='userLogout'),
    path('ready', ready, name='ready'),

]
