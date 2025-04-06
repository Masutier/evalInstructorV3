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


def noJobSchedule():
    now_date1 = datetime.now()
    now_date = now_date1.strftime("%Y-%m-%d %H:%M")
