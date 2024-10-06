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
        
