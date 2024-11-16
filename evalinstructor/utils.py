import os
import csv, json
import numpy as np
import pandas as pd
from datetime import datetime, date


# Folder to save csvs apprentice
Aprendice_destiny_path = "dbs/data/csvs/laprend"
# Folder to save csvs apprentice
instructor_destiny_path = "dbs/data/csvs/linst"
# Folder to save csvs coordinaciones
coordinador_destiny_path = "dbs/data/csvs/lcoord"
# Folder to save xlsx reportes
reporte_destiny_path = "dbs/data/reportes"


def semestre():
    now = datetime.now()
    year = now.strftime("%Y")

    if int(now.strftime("%m")) < 3:
        newDir = "_I_TRIM_" + year + "/"
    elif int(now.strftime("%m")) >3 and int(now.strftime("%m")) < 6:
        newDir = "_II_TRIM_" + year + "/"
    elif int(now.strftime("%m")) >6 and int(now.strftime("%m")) < 9:
        newDir = "_III_TRIM_" + year + "/"
    else:
        newDir = "_IV_TRIM_" + year + "/"

    return newDir


# Create df with csv files
def csvFiles(endDir):
    csv_files = []
    for file in os.listdir(endDir):
        if file.endswith('.csv'):
            csv_files.append(file)
    df = {}
    for file in csv_files:
        try:
            df[file] = pd.read_csv(endDir + file)
        except:
            df[file] = pd.read_csv(endDir + file, encoding = "ISO-8859-1")

    return csv_files, df


# crear Aprendice directorio si no existe
def crearAprendizFolder():
    newDir = semestre()
    try:
        os.makedirs(Aprendice_destiny_path + newDir)
        endDir = Aprendice_destiny_path + newDir
        return endDir
    except:
        endDir = Aprendice_destiny_path + newDir
        return endDir


# crear instructor directorio si no existe
def crearInstructorFolder():
    newDir = semestre()
    try:
        os.makedirs(instructor_destiny_path + newDir)
        endDir = instructor_destiny_path + newDir
        return endDir
    except:
        endDir = instructor_destiny_path + newDir
        return endDir

# crear Coordinador directorio si no existe
def createCoordinatorFolder():
    newDir = semestre()
    try:
        os.makedirs(coordinador_destiny_path + newDir)
        endDir = coordinador_destiny_path + newDir
        return endDir
    except:
        endDir = coordinador_destiny_path + newDir
        return endDir

def createReportFolder():
    newDir = semestre()
    try:
        os.makedirs(reporte_destiny_path + newDir)
        endDir = reporte_destiny_path + newDir
        return endDir
    except:
        endDir = reporte_destiny_path + newDir
        return endDir

# Clean file name
def clean_tbl_name(csvf):
    CleanName = csvf.upper().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","") \
        .replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ñ","N") \
        .replace("á","A").replace("é","E").replace("í","I").replace("ó","O").replace("ú","U").replace("ñ","N") \
        .replace("@","").replace("#","").replace(r"/","_").replace("\\","_").replace(r"(","").replace(")","")
    tbl_name = '{0}'.format(CleanName.split('.')[0])

    return tbl_name


def clean_columns(dataframe):
    dataframe.columns = [x.upper().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","").replace(".","") \
        .replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ñ","N") \
        .replace("á","A").replace("é","E").replace("í","I").replace("ó","O").replace("ú","U").replace("ñ","N") \
        .replace("@","").replace("#","").replace(r"/","").replace("\\","").replace(r"(","") \
        .replace(")","").replace(".","").replace("\n_anomesdia","").replace("\nanomesdia","") for x in dataframe.columns]
    
    return dataframe


def clean_data_coordinacion(dataframe):
    dataframe = clean_columns(dataframe)
    dataframe['REGION'] = dataframe['REGION'].astype(str)
    dataframe['REGION'].ffill(axis = 0)
    dataframe['CENTRO_DE_FORMACION'].ffill(axis = 0)
    dataframe['COORDINACION'].ffill(axis = 0)
    dataframe['NOMBRE_COORDINADOR'].ffill(axis = 0)
    dataframe['APELLIDOS_COORDINADOR'].ffill(axis = 0)
    dataframe['CORREO_COORDINADOR'].ffill(axis = 0)

    return dataframe


def clean_data_pregunas(dataframe):
    dataframe = clean_columns(dataframe)

    dataframe['PREGUNTA_NUMERO'] = dataframe['PREGUNTA_NUMERO'].astype(str)
    dataframe['PREGUNTA_NUMERO'].ffill(axis = 0)
    dataframe['PREGUNTA'].ffill(axis = 0)

    return dataframe


def clean_data_aprendiz(dataframe):
    dataframe = clean_columns(dataframe)

    dataframe['FICHA'] = dataframe['FICHA'].astype(str)
    dataframe['FICHA'] = [x.replace(".0","") for x in dataframe['FICHA']]
    dataframe['NUMERO_DE_DOCUMENTO'] = dataframe['NUMERO_DE_DOCUMENTO'].astype(str)
    dataframe['CELULAR'] = dataframe['CELULAR'].fillna('ND')
    dataframe['CELULAR'] = dataframe['CELULAR'].astype(str)
    dataframe['CELULAR'] = dataframe['CELULAR'].str.replace('.0', '')
    dataframe['ESTADO'] = dataframe['ESTADO'].fillna('ND')

    return dataframe


def clean_data(dataframe):
    dataframe = clean_columns(dataframe)

    dataframe['FICHA'] = dataframe['FICHA'].astype(str)
    dataframe['FICHA'].ffill(axis = 0)
    dataframe['FICHA'] = [x.replace(".0","") for x in dataframe['FICHA']]
    dataframe['PROGRAMA_DE_FORMACION'].ffill(axis = 0)
    dataframe['PROGRAMA_DE_FORMACION'] = [x.replace(".","") for x in dataframe['PROGRAMA_DE_FORMACION']]
    dataframe['TIPO_DE_DOCUMENTO'] = dataframe['TIPO_DE_DOCUMENTO'].fillna('CC')
    dataframe['NUMERO_DE_DOCUMENTO'] = dataframe['NUMERO_DE_DOCUMENTO'].astype(str)
    dataframe['NUMERO_DE_DOCUMENTO'].ffill(axis = 0)
    dataframe['NOMBRE'].ffill(axis = 0)
    dataframe['APELLIDOS'].ffill(axis = 0)

    return dataframe
