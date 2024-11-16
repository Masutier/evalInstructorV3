import os
import sqlite3 as sql3
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from dbs.dbs import *

BASE_DIR = settings.BASE_DIR


def home(request):
    try:
        sqlQuery = f"""SELECT ENDPHOTODATE FROM EvalFechas"""
        photo_date = call_db(sqlQuery)
        start_date = datetime.strptime(photo_date[0][0], '%Y-%m-%d %H:%M:%S').date()

        context = {"title": "SENA - Evaluación de instructores", "start_date": start_date}
        return render(request, "evalinstructor/home.html", context)

    except:
        context = {"title": "LogIn"}
        return render(request, "administracion/login.html", context)
    


def validarHash(request):
    if request.method == 'POST':
        hash = request.POST.get('hash')

            # Coordinacion
        try:
            sqlCoord = f"""SELECT * FROM Coordinadores WHERE HASH =?"""
            coordinador = call_db_one(sqlCoord, hash)
            if coordinador[8] == 'coordinador':
                context = {"title": "Subir Listas", "coordinador":coordinador}
                return render(request, "loadlists/loadings.html", context)
            else:
                messages.warning(request, f'El registro del Coordinador no se encontro, por favor verificar con verifique con el Centro de Producción de Soluciones Inteligentes.')
                return redirect('home')
        except:
                # Instructor
            try:
                sqlInstr = f"""SELECT * FROM Instructores WHERE HASH =?"""
                instructor = call_db_one(sqlInstr, hash)
                if instructor[10] == 'instructor':
                    context = {"title": "Subir Foto", "instructor":instructor}
                    return render(request, "loadlists/uploadPhoto.html", context)
                else:
                    messages.warning(request, f'El registro del instructor no se encontro, por favor verificar con su coordinación.')
                    return redirect('home')
            except:
                    # Aprendiz
                try:
                    sqlApren = f"""SELECT * FROM Aprendices WHERE HASH =?"""
                    aprendiz = call_db_one(sqlApren, hash)
                    if aprendiz[10] == 'aprendiz':
                        return redirect("obtener_datos_aprendiz", pk=hash)
                    else:
                        messages.warning(request, f'El registro del aprendiz no se encontro, por favor verificar con su instructor.')
                        return redirect('home')
                except:
                    messages.warning(request, f'El hash ingresado no se encontro, intentelo otra vez')
                    return redirect('home')


def about(request):
    context = {"title": "SENA - Evaluación de instructores"}
    return render(request, "evalinstructor/about.html", context)


def recuperacion(request):
    if request.method == "POST":
        try:
            numero_de_documento = request.POST.get('numero_de_documento')
            sqlApren =  """SELECT * FROM aprendices WHERE NUMERO_DE_DOCUMENTO =? """
            aprendiz = call_db_one(sqlApren, numero_de_documento)
            no_habilitado = aprendiz[11]
            
            if aprendiz and no_habilitado == 'NA':
                    context = {"title": "Recuperacion Hash" , 'aprendiz': aprendiz}
                    return render(request, "evalinstructor/hashrecup.html", context)
            else:
                messages.warning(request, f'El numero de documento no coincide o El usuario se encuentra deshabilitado')
                return render(request, "evalinstructor/hashrecup.html")
        except:
            messages.warning(request, f'El numero de documento no se encuenta registrado')
            return redirect('home')
    else:
        context = {"title": "Recuperacion Hash"}
        return render(request, "evalinstructor/hashrecup.html", context)
