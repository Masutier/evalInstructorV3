import os
import hashlib
import sqlite3 as sql3
import openpyxl
import xlsxwriter
import mimetypes
from io import BytesIO as IO
from django.http.response import HttpResponse
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from evalinstructor.utils import *
from dbs.dbs import *

BASE_DIR = settings.BASE_DIR
timing = datetime.today().date()


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('administracion')
        else:
            messages.info(request, f'Algo no salio bien, Intentelo otra vez')
            return redirect('/')
    context = {"title": "LogIn"}
    return render(request, "administracion/login.html", context)


def userLogout(request):
    logout(request)
    return redirect('/')


def administracion(request):
    instructorescc = []
    instconfoto = []
    instsinfoto = []
    sqlCoord = f"""SELECT * FROM Coordinadores"""
    sqlInstr = f"""SELECT * FROM Instructores"""
    sqlApren = f"""SELECT * FROM Aprendices"""
    sqlDates = f"""SELECT * FROM EvalFechas"""
    try:
            # Coordinaciones db
        coordinaciones = call_db(sqlCoord)
        coordqty = len(coordinaciones)
            # Fechas db
        evalFechas = call_db(sqlDates)
            # Calculate dates
        startdate = evalFechas[0][0]
        endCoordination = evalFechas[0][1]
        endInstPhoto = evalFechas[0][2]
        endEvaluation = evalFechas[0][3]
        
            # Instructores db
        instructoresAll = call_db(sqlInstr)
        for instructorAll in instructoresAll:
            instructorescc.append(instructorAll[6])
            if instructorAll[12] != 'static/img/img/person.jpg':
                instconfoto.append(instructorAll[6])
            else:
                instsinfoto.append(instructorAll[6])
        instrucqty = len(set(instructorescc))
        instconfotoqty = len(set(instconfoto))
        instsinfotoqty = len(set(instsinfoto))
            # Aprendices db
        aprendqty = len(call_db(sqlApren))

        context = {'title':'Administracion', 
                    'coordinaciones':coordinaciones, 
                    'coordqty':coordqty, 
                    'startdate':startdate, 
                    'endCoordination':endCoordination, 
                    'endInstPhoto':endInstPhoto,
                    'endEvaluation':endEvaluation, 
                    'instrucqty':instrucqty,
                    'instconfotoqty':instconfotoqty,
                    'instsinfotoqty':instsinfotoqty,
                    'aprendqty':aprendqty }
        return render(request, 'administracion/administracion.html', context)
    except:
        try:
                # Coordinaciones db
            coordinaciones = call_db(sqlCoord)
            coordqty = len(coordinaciones)
                # Fechas db
            evalFechas = call_db(sqlDates)
                # Calculate dates
            startdate = evalFechas[0][0]
            endCoordination = evalFechas[0][1]
            endInstPhoto = evalFechas[0][2]
            endEvaluation = evalFechas[0][3]
                # Instructores db
            instructoresAll = call_db(sqlInstr)
            for instructorAll in instructoresAll:
                instructorescc.append(instructorAll[6])
                if instructorAll[12] != 'static/img/img/person.jpg':
                    instconfoto.append(instructorAll[6])
                else:
                    instsinfoto.append(instructorAll[6])
            instrucqty = len(set(instructorescc))
            instconfotoqty = len(set(instconfoto))
            instsinfotoqty = len(set(instsinfoto))

            context = {'title':'Administracion', 
                        'coordinaciones':coordinaciones, 
                        'coordqty':coordqty, 
                        'startdate':startdate, 
                        'endCoordination':endCoordination, 
                        'endInstPhoto':endInstPhoto,
                        'endEvaluation':endEvaluation, 
                        'instrucqty':instrucqty,
                        'instconfotoqty':instconfotoqty,
                        'instsinfotoqty':instsinfotoqty,
                        'aprendqty':"Not Setup" }
            return render(request, 'administracion/administracion.html', context)
        except:
            try:
                    # Coordinaciones db
                coordinaciones = call_db(sqlCoord)
                coordqty = len(coordinaciones)
                    # Fechas db
                evalFechas = call_db(sqlDates)
                    # Calculate dates
                startdate = evalFechas[0][0]
                endCoordination = evalFechas[0][1]
                endInstPhoto = evalFechas[0][2]
                endEvaluation = evalFechas[0][3]
                    # Crear tabla Informes
                context = {'title':'Administracion', 
                            'coordinaciones':coordinaciones, 
                            'coordqty':coordqty, 
                            'startdate':startdate, 
                            'endCoordination':endCoordination, 
                            'endInstPhoto':endInstPhoto,
                            'endEvaluation':endEvaluation, 
                            'instrucqty':"Not Setup",
                            'instconfotoqty':"Not Setup",
                            'instsinfotoqty':"Not Setup",
                            'aprendqty':"Not Setup" }
                return render(request, 'administracion/administracion.html', context)
            except:
                messages.warning(request, f'Todo parece indicar que la aplicación no ha sido activada.')
                return redirect('loadActivation')


def ready(request):
    from jobs import allSchedulers
    fullMixTable(request)
    allSchedulers.start()

    messages.info(request, f'Se creo la tabla de "Informes" y se activaron los Schedules')
    return redirect('administracion')


def createFinalReportFicha(request):
    inform = []
    fullTableFichaInstructor(request)
    sqlquery = "SELECT * FROM VRESULTADOSXFICHA"
    informe = call_db(sqlquery)

    for info in informe:
        info = list(info)
        diction = {"DOCAPRENDIZ":info[0], "DOCINSTRUCTOR":info[1], "FICHA":info[2],
                    "P1":info[3], "P2":info[4], "P3":info[5], "P4":info[6], "P5":info[7], "P6":info[8], "P7":info[9], "P8":info[10], "P9":info[11], "P10":info[12], "P11":info[13], "P12":info[14]}
        inform.append(diction)

    dfficha = pd.DataFrame(inform)
        # create directorio si no existe

    endDir = createReportFolder()
        # save to xlsx
    dfficha.to_excel(endDir + "reporte_FinalporFicha_" + str(timing) + ".xlsx", index=False)

    filename = "reporte_FinalporFicha_" + str(timing) + ".xlsx"
    file_path = os.path.join(endDir, filename)

        # Verifica si el archivo existe
    if not os.path.exists(file_path):
        messages.error(request, 'El archivo no se encontró.')
        return redirect('administracion')

        # Crea la respuesta para descargar el archivo
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = os.path.getsize(file_path)

    messages.info(request, 'Archivo descargado exitosamente.')
    return response

def createFinalReportDocumento(request):
    inform2 = []
    fullTableDocInstructor(request)
    sqlquery = "SELECT * FROM VRESULTADOTOTAL"
    informe2 = call_db(sqlquery)

    for info2 in informe2:
        info2 = list(info2)
        diction2 = {"DOCAPRENDIZ":info2[0], "DOCINSTRUCTOR":info2[1],
                    "P1":info2[2], "P2":info2[3], "P3":info2[4], "P4":info2[5], "P5":info2[6], "P6":info2[7], "P7":info2[8], "P8":info2[9], "P9":info2[10], "P10":info2[11], "P11":info2[12], "P12":info2[13]}
        inform2.append(diction2)

        # create directorio si no existe
    dfdocumento = pd.DataFrame(inform2)

    endDir = createReportFolder()
        # save to xlsx
    dfdocumento.to_excel(endDir + "reporte_FinalporDocumento_" + str(timing) + ".xlsx", index=False)

    filename2 = "reporte_FinalporDocumento_" + str(timing) + ".xlsx"
    file_path = os.path.join(endDir, filename2)

        # Verifica si el archivo existe
    if not os.path.exists(file_path):
        messages.error(request, 'El archivo no se encontró.')
        return redirect('administracion')

        # Crea la respuesta para descargar el archivo
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename2}"'
        response['Content-Length'] = os.path.getsize(file_path)

    messages.info(request, 'Archivo descargado exitosamente.')
    return response
