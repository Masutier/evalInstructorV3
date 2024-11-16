import os
import hashlib
import pandas as pd
import sqlite3 as sql3
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage, get_connection, send_mass_mail
from evalinstructor.utils import *
from dbs.dbs import *
from jobs.mail import sendMailCoordinaciones
from .forms import UploadFilesForm

BASE_DIR = settings.BASE_DIR
timing = datetime.today().date()
dateEndCoordination = 15
dateEndPhoto = dateEndCoordination + 7
dateEndEvalua = dateEndCoordination + 7 + 15


def loadActivation(request):
    context = {"title": "Subir Archivo de Activación"}
    return render(request, "loadlists/loadActivation.html", context)


def activation(request):
    global startdateDf
    if request.method == "POST":
            # Get file and split for extension
        fileinn = request.FILES["instructorFileIn"]
        nameFile = fileinn.name
        filenamex = nameFile.split('.')
            # check if file is excel
        if filenamex[-1] == "xls" or filenamex[-1] == "xlsx":
            dataframe = pd.read_excel(fileinn, 'Coordinaciones') 
        else:
            messages.info(request, f'El archivo a precesar no es archivo excel, verifique que sea excel')
            return redirect('/')
            # Extraer info de las Coordinaciones
            # Delete first 2 rows from file
        dfcoord = dataframe.drop(dataframe.index[0:1])
        dfcoord.reset_index(drop=True, inplace=True)
        dfcoord.columns = dfcoord.iloc[0]
        dfcoord = dfcoord[1:8]
        dfcoord = clean_data_coordinacion(dfcoord)
        dfcoord = dfcoord.dropna()
            # create hash and assign group para Coordinaciones
        for i, row in dfcoord.iterrows():
            val = row['COORDINACION'] + row['NOMBRE_COORDINADOR'] + row['APELLIDOS_COORDINADOR'] + row['CORREO_COORDINADOR']
            dfcoord.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()
                # create Group
            dfcoord.at[i, 'GRUPO'] = "coordinador"
            centroFormacion = row['CENTRO_DE_FORMACION']
        dfcoord['FECHA_DE_UPLOAD'] = datetime.today().strftime('%m/%d/%Y %H:%M:%S')
            # Extract questions
        dfquestion = pd.read_excel(fileinn, 'Preguntas') 
        dfquestion = dfquestion.drop(dfquestion.index[0:1])
        dfquestion.reset_index(drop=True, inplace=True)
        dfquestion.columns = dfquestion.iloc[0]
        dfquestion = dfquestion[1:13]
        dfquestion = clean_data_pregunas(dfquestion)
            # Calculate dates
        startdateDf = dfcoord.at[1, 'FECHA_DE_COMIENZO']
        endCoordination = startdateDf + timedelta(days=dateEndCoordination)
        endInstPhoto = startdateDf + timedelta(days=dateEndPhoto)
        endEvaluation = startdateDf + timedelta(days=dateEndEvalua)
        times = {"STARTDATE": startdateDf,
                "ENDCOORDATE": endCoordination,
                "ENDPHOTODATE": endInstPhoto,
                "ENDEVALUACION": endEvaluation }
        evalDates = pd.DataFrame([times])
            # crear directorio si no existe
        endDir = createCoordinatorFolder()
            # save to Coordinaciones csv
        dfcoord.to_csv(endDir + "Coordinacion_" + centroFormacion + "_" + str(timing) + ".csv", index=False)
            # save to questions csv
        dfquestion.to_csv(endDir + "Preguntas_" + centroFormacion + "_"  + str(timing) + ".csv", index=False)
            # DATABASE Coordinaciones
        save_db(dfcoord, "Coordinadores")
            # DATABASE questions
        save_db(dfquestion, "Preguntas")
            # DATABASE Evaluacion
        save_db(evalDates, "EvalFechas")
            # Send Mail to Coordinations
        sendMailCoordinaciones()

    return redirect("administracion")


def loadings(request):
    sqlQuery = f"""SELECT * FROM Coordinadores"""
    coordinaciones = call_db(sqlQuery)

    context = {'title': 'Subir Listas'}
    return render(request, 'loadlists/loadings.html', context)


def loadInstructores(request):
    if request.method == "POST":
            # Recibe file y separa nombre de la extension
        fileinn = request.FILES["instructorFileIn"]
        nameFile = fileinn.name
        filenamex = nameFile.split('.')
            # check if file is excel
        if filenamex[-1] == "xls" or filenamex[-1] == "xlsx":
            dataframe = pd.read_excel(fileinn) 
        else:
            messages.info(request, f'El archivo a precesar no es archivo excel, verifique que sea excel')
            return redirect('/')
            # Extract location info for Instructores
        REGION = dataframe.loc[0,:].values[3]
        CENTRO_DE_FORMACION = dataframe.loc[0,:].values[4]
        COORDINACION = dataframe.loc[0,:].values[5]
            # Extract and Delete unused info from file
        dfinstructor = dataframe.drop(dataframe.index[0:2])
        dfinstructor.reset_index(drop=True, inplace=True)
        dfinstructor.columns = dfinstructor.iloc[0]
        dfinstructor = clean_data(dfinstructor)
        dfinstructor = dfinstructor.dropna()
        dfinstructor = dfinstructor.drop(0)
        dfinstructor.reset_index(drop=True, inplace=True)
            # create hash
        for i, row in dfinstructor.iterrows():
            val = row['NUMERO_DE_DOCUMENTO'] + row['NOMBRE'] + row['APELLIDOS']
            dfinstructor.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()
            # create extra info
        dfinstructor['GRUPO'] = 'instructor'
        dfinstructor['ESTADO'] = 0
        dfinstructor['PHOTO'] = 'static/img/img/person.jpg'
        dfinstructor['REGION'] = REGION
        dfinstructor['CENTRO_DE_FORMACION'] = CENTRO_DE_FORMACION
        dfinstructor['COORDINACION'] = COORDINACION
        dfinstructor['FECHA_DEL_REPORTE'] = datetime.now()
        dfinstructor.reset_index(drop=True, inplace=True)
            # create directorio si no existe
        endDir = crearInstructorFolder()
            # DATABASE instructores
        save_db(dfinstructor, "Instructores")
            # save to csv
        dfinstructor.to_csv(endDir + "instructores_" + str(timing) + ".csv", index=False)
        messages.warning(request, f'El registro de las listas de los instructores se realizo exitosamente.')

    return redirect("home")



def loadAprendicesMany(request):
    data_to_display = None
    listxx=[]
    allApren = []
    ficha = ""
    lenficha = 6

    if request.method == 'POST':
        files = request.FILES.getlist('aprendfileinn')
        
        for file in files:
            data = pd.read_excel(file)
                # Get fecha 
            fechaReporte = data.iat[2,2]
                # Get ficha number
            celx = data.iat[0,2]
            ficha = celx[0:7]
                # Delete first 4 rows from file
            data = data.drop(data.index[0:3])
            data.reset_index(drop=True, inplace=True)
            data.drop(index=4)
            data.columns = data.iloc[0]
            data = data[1:]
                # Add columns for fechaReporte and ficha
            data['ficha'] = ficha
            data['fecha_del_reporte'] = fechaReporte
            allApren.append(data)

        if not allApren:
            messages.warning(request, f'No se encontraron listados o algo salio mal, revise que los listados esten el la carpeta "Descargas/Listados/" o "Downloads/Listados/.')
            return redirect('home')

            # Join all files in one dataframe
        dataframe = pd.concat(allApren, axis=0)
        dataframe.reset_index(drop=True, inplace=True)
            # clean columns names and data
        dataframe = clean_data_aprendiz(dataframe)
            # create HASH column
        dataframe['HASH'] = dataframe.apply(lambda x: hashlib.md5(x['NUMERO_DE_DOCUMENTO'].encode() + x['NOMBRE'].encode() + x['APELLIDOS'].encode()).hexdigest(), axis=1)
            # crear grupo
        dataframe['GRUPO'] = 'aprendiz'
            # Create "NO_ABILITADO" column, check if "ESTADO" is valid to perform the evaluation and Remove "NUMERO_DE_DOCUMENTO"
        dataframe['NO_HABILITADO'] = "NA"
        dataframe.loc[dataframe.ESTADO == 'RETIRO VOLUNTARIO', 'NO_HABILITADO'] = dataframe.CORREO_ELECTRONICO
        dataframe.loc[dataframe.ESTADO == 'TRASLADADO', 'NO_HABILITADO'] = dataframe.CORREO_ELECTRONICO
        dataframe.loc[dataframe.ESTADO == 'APLAZADO', 'NO_HABILITADO'] = dataframe.CORREO_ELECTRONICO
        dataframe.loc[dataframe.ESTADO == 'CANCELADO', 'NO_HABILITADO'] = dataframe.CORREO_ELECTRONICO
        dataframe.loc[dataframe.NO_HABILITADO == dataframe.CORREO_ELECTRONICO, 'HASH'] = "NA"
        dataframe.loc[dataframe.NO_HABILITADO == dataframe.CORREO_ELECTRONICO, 'CORREO_ELECTRONICO'] = "NA"
            # DATABASE
        save_db(dataframe, "Aprendices")
            # Create directory if not exists
        endDir = crearAprendizFolder()
            # save to csv
        dataframe.to_csv(endDir + "aprendices_" + str(timing) + ".csv", index=False)
        messages.warning(request, f'El registro de las listas de los aprendices se realizo exitosamente.')

    return redirect("home")


def uploadPhoto(request):
    sqlInstr = f"""SELECT * FROM Instructores WHERE NUMERO_DE_DOCUMENTO =?"""
    sqlQuery = f"""UPDATE Instructores SET PHOTO = ? WHERE NUMERO_DE_DOCUMENTO =?"""
    if request.method == 'POST' and request.FILES['PHOTO']:
        myfile = request.FILES['PHOTO']
        numero_de_documento = request.POST.get('NUMERO_DE_DOCUMENTO')

        try:
                # Get inst
            instructor = call_db_one(sqlInstr, numero_de_documento)

            fs = FileSystemStorage()
            filename = fs.save(numero_de_documento, myfile)
            uploaded_file_url = fs.url(filename)
                # Save in db
            update_db(sqlQuery, uploaded_file_url, numero_de_documento)
                # Re-call instructor
            instructor = call_db_one(sqlInstr, numero_de_documento)

            context = {'instructor': instructor}
            return render(request, 'loadlists/instructor.html', context)
        except:
            messages.warning(request, f'El Instructor no se encontro en los registros.')
            return redirect('home')

    context = {'title': "Load Foto"}
    return render(request, 'loadlists/uploadPhoto.html', context)

def createFinalPorCoordinacion(request, data):
    dataeval = "SELECT ENDEVALUACION FROM EvalFechas"
    endDate = call_db(dataeval)
    timing = datetime.now()  
    timing_str = timing.strftime('%Y-%m-%d_%H-%M-%S')  

    if endDate and len(endDate) > 0:
        endDate = endDate[0][0]  
        print(f"Fecha de fin de evaluación: {endDate}")
        try:
            if isinstance(endDate, str):
                endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        print(f"Fecha endDate (fin evaluación): {endDate}, Fecha actual timing: {timing}")

        if endDate < timing:  
            inform2 = []
            fullTableCordInstructor(request)
            sqlquery = "SELECT * FROM VRESULTADOSXCOORDINACION WHERE COORDINACION = ?"
            informe2 = call_db_all(sqlquery, data)

            for info2 in informe2:
                info2 = list(info2)
                diction2 = {
                    "DOCAPRENDIZ": info2[0], "DOCINSTRUCTOR": info2[1], "COORDINACION": info2[2],
                    "P1": info2[3], "P2": info2[4], "P3": info2[5], "P4": info2[6], "P5": info2[7],
                    "P6": info2[8], "P7": info2[9], "P8": info2[10], "P9": info2[11], "P10": info2[12],
                    "P11": info2[13], "P12": info2[14]
                }
                inform2.append(diction2)

            dfdocumento = pd.DataFrame(inform2)
            endDir = createReportFolder()
            dfdocumento.to_excel(endDir + f"reporte_Final_{timing_str}.xlsx", index=False)

            filename2 = f"reporte_Final_{timing_str}.xlsx"
            file_path = os.path.join(endDir, filename2)

            if not os.path.exists(file_path):
                messages.error(request, 'El archivo no se encontró.')
                return response

            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{filename2}"'
                response['Content-Length'] = os.path.getsize(file_path)

            messages.info(request, 'Archivo descargado exitosamente.')
            return response
        else:
            print("La evaluación aún está en proceso.")
            messages.info(request, 'Aún se encuentra la evaluación en proceso.')
            return redirect('home')
    else:
        messages.error(request, 'No se pudo obtener la fecha de fin de evaluación.')
        return redirect('home')

    return redirect('home')