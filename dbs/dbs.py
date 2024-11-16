import os
import pandas as pd
import sqlite3 as sql3
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

BASE_DIR = settings.BASE_DIR


def save_db(dataframe, table):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dataframe.to_sql(name=table, con=conn, if_exists="replace", index=False)
    conn.close()


def save_response(dataframe, table):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dataframe.to_sql(name=table, con=conn, if_exists="append", index=False)
    conn.close()


def call_db(sqlQuery):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery,).fetchall()
    conn.close()
    return dbData


def call_db_one(sqlQuery, adition):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery, (adition,)).fetchone()
    conn.close()
    return dbData

def call_db_all2(sqlQuery, data1, data2):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery, (data1, data2)).fetchall()
    conn.close()
    return dbData


def call_db_all(sqlQuery, *params):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery, params).fetchall()
    conn.close()
    return dbData


def call_db_con(sqlQuery, adition):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery, (adition,)).fetchall()
    conn.close()
    return dbData


def call_db_two_all(sqlQuery, data1, data2):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery, (data1, data2)).fetchall()
    conn.close()
    return dbData


def createTable(sqlQuery):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    cur = conn.cursor()
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()


def update_db(sqlQuery, data1, data2):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    cur = conn.cursor()
    cur.execute(sqlQuery, (data1, data2))
    conn.commit()
    conn.close()


def updateInforme(sqlQuery):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    cur = conn.cursor()
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()


def fullMixTable(request):
    sql = "SELECT * FROM Preguntas"
    preguntas = call_db(sql)

        # DATABASE Informe
    sqlQuery = """ CREATE TABLE Informe (
        FICHA TEXT NOT NULL, 
        DOCAPRENDIZ TEXT NOT NULL, 
        APRENDIZ_NAME TEXT NOT NULL, 
        APRENDIZ_LAST TEXT NOT NULL, 
        DOCINSTRUCTOR TEXT NOT NULL, 
        INSTRUCTOR_NAME TEXT NOT NULL, 
        INSTRUCTOR_LAST TEXT NOT NULL, 
        P1 TEXT NOT NULL, 
        P2 TEXT NOT NULL, 
        P3 TEXT NOT NULL, 
        P4 TEXT NOT NULL, 
        P5 TEXT NOT NULL, 
        P6 TEXT NOT NULL, 
        P7 TEXT NOT NULL, 
        P8 TEXT NOT NULL, 
        P9 TEXT NOT NULL, 
        P10 TEXT NOT NULL, 
        P11 TEXT NOT NULL, 
        P12 TEXT NOT NULL
        )"""
    
    try:
        createTable(sqlQuery)
    except:
        messages.info(request, f'La Tabla "Informe" ya existe!')


def fullTableFichaInstructor(request):
        # DATABASE Informe
    sqlQuery = """ CREATE VIEW VRESULTADOSXFICHA AS
            SELECT DOCINSTRUCTOR,INSTRUCTOR_NAME,r.FICHA,
            (SELECT ROUND(AVG(P1)*100/5)) P1,
            (SELECT ROUND(AVG(P2)*100/5)) P2,
            (SELECT ROUND(AVG(P3)*100/5)) P3,
            (SELECT ROUND(AVG(P4)*100/5)) P4,
            (SELECT ROUND(AVG(P5)*100/5)) P5,
            (SELECT ROUND(AVG(P6)*100/5)) P6,
            (SELECT ROUND(AVG(P7)*100/5)) P7,
            (SELECT ROUND(AVG(P8)*100/5)) P8,
            (SELECT ROUND(AVG(P9)*100/5)) P9,
            (SELECT ROUND(AVG(P10)*100/5)) P10,
            (SELECT ROUND(AVG(P11)*100/5)) P11,
            (SELECT ROUND(AVG(P12)*100/5)) P12
            FROM Informe r
            JOIN INSTRUCTORES I
            on I.NUMERO_DE_DOCUMENTO=r.DOCINSTRUCTOR 
            GROUP BY r.DOCINSTRUCTOR, r.INSTRUCTOR_NAME, r.FICHA
            """
    try:
        createTable(sqlQuery)
    except:
        messages.info(request, f'La Tabla "ReportePorFicha" ya existe!')

def fullTableDocInstructor(request):
        # DATABASE Informe
    sqlQuery = """ CREATE VIEW VRESULTADOTOTAL AS
            SELECT DISTINCT DOCINSTRUCTOR,INSTRUCTOR_NAME,
            (SELECT ROUND(AVG(P1)*100/5)) P1,
            (SELECT ROUND(AVG(P2)*100/5)) P2,
            (SELECT ROUND(AVG(P3)*100/5)) P3,
            (SELECT ROUND(AVG(P4)*100/5)) P4,
            (SELECT ROUND(AVG(P5)*100/5)) P5,
            (SELECT ROUND(AVG(P6)*100/5)) P6,
            (SELECT ROUND(AVG(P7)*100/5)) P7,
            (SELECT ROUND(AVG(P8)*100/5)) P8,
            (SELECT ROUND(AVG(P9)*100/5)) P9,
            (SELECT ROUND(AVG(P10)*100/5)) P10,
            (SELECT ROUND(AVG(P11)*100/5)) P11,
            (SELECT ROUND(AVG(P12)*100/5)) P12
            FROM Informe
            GROUP BY DOCINSTRUCTOR, INSTRUCTOR_NAME
            """
    try:
        createTable(sqlQuery)
    except:
        messages.info(request, f'La Tabla "ReportePorDocumento" ya existe!')

def fullTableCordInstructor(request):
        # DATABASE Informe
    sqlQuery = """ CREATE VIEW VRESULTADOSXCOORDINACION AS
            SELECT DOCINSTRUCTOR,INSTRUCTOR_NAME, I.COORDINACION,
            (SELECT ROUND(AVG(P1)*100/5)) P1,
            (SELECT ROUND(AVG(P2)*100/5)) P2,
            (SELECT ROUND(AVG(P3)*100/5)) P3,
            (SELECT ROUND(AVG(P4)*100/5)) P4,
            (SELECT ROUND(AVG(P5)*100/5)) P5,
            (SELECT ROUND(AVG(P6)*100/5)) P6,
            (SELECT ROUND(AVG(P7)*100/5)) P7,
            (SELECT ROUND(AVG(P8)*100/5)) P8,
            (SELECT ROUND(AVG(P9)*100/5)) P9,
            (SELECT ROUND(AVG(P10)*100/5)) P10,
            (SELECT ROUND(AVG(P11)*100/5)) P11,
            (SELECT ROUND(AVG(P12)*100/5)) P12
            FROM Informe r
            JOIN INSTRUCTORES I
            on I.NUMERO_DE_DOCUMENTO=r.DOCINSTRUCTOR 
            GROUP BY r.DOCINSTRUCTOR, r.INSTRUCTOR_NAME, I.COORDINACION
            """
    try:
        createTable(sqlQuery)
    except:
        messages.info(request, f'La Tabla "ReporteFinal" ya existe!')