import json
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from dbs.dbs import call_db
from .mail import *


def sendMailInstructores():
    data = "Instructores"
    sendInstructorAskPhoto()
    
    sendComfirmation(data)


def sendMailAprendices():
    # sqlAprendices = f"""SELECT * FROM Aprendices"""
    # allAprendices = call_db(sqlAprendices)

    # if len(allAprendices) > 400:

    #     # Take all data in chunks of 400 registers

    #     for aprendiz in allAprendices400:
    #         data = "Aprendices"
    #         sendInstructorAskPhoto()


    # sendComfirmation(data)
    sqlQuery2 = f"""SELECT * FROM EvalFechas"""
    evalFechas = call_db(sqlQuery2)
    data = "Data para el correo de Aprendices"

    mailData = {'destiny':data, 'endInstPhoto':evalFechas[0][2], 'endEvaluation':evalFechas[0][3], 
                'MAIL_ADDRESS': "gmasutier77@gmail.com", 'subject': "Recordatorio de envio de correos"}

    sendMailAprendicesEval(mailData)


def noJobSchedule():
    sqlDates = f"""SELECT * FROM EvalFechas"""
    allDates = call_db(sqlDates)
    startDate = allDates[0][0]

    run_date1 = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
    now_date1 = datetime.now()

    run_date = run_date1.strftime("%Y-%m-%d %H:%M")
    now_date = now_date1.strftime("%Y-%m-%d %H:%M")

    print('SETUP TIME ', run_date)
    print('TIME NOW ', now_date)