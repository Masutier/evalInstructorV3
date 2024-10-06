import os
import hashlib
import sqlite3 as sql3
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
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


def createFinalReport(request):
    inform = []
    sqlquery = "SELECT * FROM Informe"
    informe = call_db(sqlquery)

    for info in informe:
        info = list(info)
        prom = (int(info[7]) + int(info[8]) + int(info[9]) + int(info[10]) + int(info[11]) + int(info[12]) + int(info[13]) + int(info[14]) + int(info[15]) + int(info[16]) + int(info[17]) + int(info[18]))/12
        diction = {"FICHA":info[0], "DOCAPRENDIZ":info[1], "APRENDIZ_NAME":info[2], "APRENDIZ_LAST":info[3], "DOCINSTRUCTOR":info[4], "INSTRUCTOR_NAME":info[5], "INSTRUCTOR_LAST":info[6],
                    "P1":info[7], "P2":info[8], "P3":info[9], "P4":info[10], "P5":info[11], "P6":info[12], "P7":info[13], "P8":info[14], "P9":info[15], "P10":info[16], "P11":info[17], "P12":info[18], "FINAL":prom}
        inform.append(diction)

    df = pd.DataFrame(inform)
        # create directorio si no existe
    endDir = createReportFolder()
        # save to xlsx
    df.to_excel(endDir + "reporte_general_" + str(timing) + ".xlsx", index=False)
    filename = "reporte_general_" + str(timing) + ".xlsx"
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

    messages.info(request, 'Archivo General descargado exitosamente.')
    return response


def createReportInstructor(request):
    count = 0
    totalInstructor = 0
    inform = []
    instructores = []
    totalInstructor2 = []
    sqlquery = "SELECT * FROM Informe"
    informe = call_db(sqlquery)

    for info in informe:
        info = list(info)
        prom = (int(info[7]) + int(info[8]) + int(info[9]) + int(info[10]) + int(info[11]) + int(info[12])
                 + int(info[13]) + int(info[14]) + int(info[15]) + int(info[16]) + int(info[17]) + int(info[18]))/12
        diction = {"FICHA":info[0], "DOCAPRENDIZ":info[1], "APRENDIZ_NAME":info[2], "APRENDIZ_LAST":info[3], 
                    "DOCINSTRUCTOR":info[4], "INSTRUCTOR_NAME":info[5], "INSTRUCTOR_LAST":info[6],
                    "P1":info[7], "P2":info[8], "P3":info[9], "P4":info[10], "P5":info[11], "P6":info[12], 
                    "P7":info[13], "P8":info[14], "P9":info[15], "P10":info[16], "P11":info[17], "P12":info[18], "FINAL":prom}
        inform.append(diction)
        if info[4] not in instructores:
            instructores.append(info[4])

    for instructor in instructores:
        for info in inform:
            if info['DOCINSTRUCTOR'] == str(instructor):
                count += 1
                totalInstructor += info['FINAL']
                instructor_name = info['INSTRUCTOR_NAME']
                instructor_last = info['INSTRUCTOR_LAST']

        totalInstructor = totalInstructor / count
        totalInstructor2.append({'DOCINSTRUCTOR':instructor, 'INSTRUCTOR_NAME':instructor_name, 'INSTRUCTOR_LAST':instructor_last, 'APRENDICES_EVALUARON':count, 'PROMEDIO_TOTAL':totalInstructor})
        totalInstructor = 0
        count = 0

        # create dataframe
    df = pd.DataFrame(totalInstructor2)
        # create directorio si no existe
    endDir = createReportFolder()
        # save to xlsx
    df.to_excel(endDir + "reporte_por_instructor_" + str(timing) + ".xlsx", index=False)
    filename = "reporte_por_instructor_" + str(timing) + ".xlsx"
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

    messages.info(request, 'Archivo de Instructores descargado exitosamente.')
    return response
