import os
import sqlite3 as sql3
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from dbs.dbs import *
from django.views.decorators.cache import cache_control
from django.utils import timezone
from django.urls import reverse


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def obtener_datos_aprendiz(request, pk):
    sql = "SELECT * FROM Aprendices WHERE HASH = ?"
    aprendiz = call_db_one(sql, pk)

    if aprendiz:
        ficha = aprendiz[7]
        num_doc_aprendiz = aprendiz[1]
        sql = """
        SELECT * FROM Instructores 
        WHERE FICHA = ? AND 
        NUMERO_DE_DOCUMENTO NOT IN (
            SELECT DOCINSTRUCTOR FROM Informe WHERE DOCAPRENDIZ = ?
        )
        """
        instructo = call_db_all(sql, ficha, num_doc_aprendiz)

        if not instructo:
            messages.error(request, f"Ya no tienes más instructores por evaluar")
            return redirect('home') 

    context = {"title": "Evaluar Instructores", "aprendiz": aprendiz, "instructo": instructo}
    response = render(request, 'evaluaciones/aprendiz.html', context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response

    # context = {"title": "Evaluar Instructores", "aprendiz": aprendiz, "instructo": instructo}
    # return render(request, 'evaluaciones/aprendiz.html', context)


def obtener_preguntas(request, pk, pk2):   
    sql = "SELECT * FROM Preguntas"
    preguntas = call_db(sql)

    sql = "SELECT * FROM Instructores WHERE NUMERO_DE_DOCUMENTO = ?"
    instructor = call_db_one(sql, pk)

    sql = "SELECT * FROM Aprendices WHERE NUMERO_DE_DOCUMENTO = ?"
    aprendiz = call_db_one(sql, pk2)

    context = {"title": "Preguntas", "preguntas": preguntas, "instructor": instructor, "aprendiz": aprendiz}
    return render(request, 'evaluaciones/preguntas.html', context)


def guardar_respuestas(request, pk, pk2):
    if request.method == "POST":
        query1 = "SELECT * FROM Aprendices WHERE NUMERO_DE_DOCUMENTO = ?"
        aprendiz = call_db_one(query1, pk2)
        
        query2 = "SELECT * FROM Instructores WHERE NUMERO_DE_DOCUMENTO = ?"
        instructor = call_db_one(query2, pk)

        sql_check = """
        SELECT * FROM Informe 
        WHERE DOCAPRENDIZ = ? AND DOCINSTRUCTOR = ?
        """
        evaluacion_existente = call_db_all(sql_check, pk2, pk)
        
        if evaluacion_existente:
            messages.error(request, "Ya has evaluado a este instructor.")
            return redirect('obtener_datos_aprendiz', pk=aprendiz[9])
        
        respuestas = request.POST
        respuestas_data = {
            "FICHA": instructor[0],
            "DOCAPRENDIZ": pk2,
            "APRENDIZ_NAME": aprendiz[2],
            "APRENDIZ_LAST": aprendiz[3],
            "DOCINSTRUCTOR": instructor[6],
            "INSTRUCTOR_NAME": instructor[3],
            "INSTRUCTOR_LAST": instructor[4],
            "P1": respuestas.get('1'),
            "P2": respuestas.get('2'),
            "P3": respuestas.get('3'),
            "P4": respuestas.get('4'),
            "P5": respuestas.get('5'),
            "P6": respuestas.get('6'),
            "P7": respuestas.get('7'),
            "P8": respuestas.get('8'),
            "P9": respuestas.get('9'),
            "P10": respuestas.get('10'),
            "P11": respuestas.get('11'),
            "P12": respuestas.get('12'),
        }

        evalInstr = pd.DataFrame([respuestas_data])
        save_response(evalInstr, "Informe")
       
        hash = aprendiz[9] 
        return redirect('obtener_datos_aprendiz', pk=hash)
    


    