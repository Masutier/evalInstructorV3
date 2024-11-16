import sqlite3 as sql3
from datetime import datetime, date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from .jobs import *
from dbs.dbs import *


def setup():
    #count = count + 1
    try:
        sqlDates = f"""SELECT * FROM EvalFechas"""
        allDates = call_db(sqlDates)

        startDate = allDates[0][0]
        StartDX = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8, minutes=30)
        StartD = split_date(StartDX)

        startInst = allDates[0][1]
        InstrDX = datetime.strptime(startInst, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8, minutes=30)
        InstrD = split_date(InstrDX)

        startApre = allDates[0][2]
        AprenDX = datetime.strptime(startApre, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8, minutes=30)
        AprenD = split_date(AprenDX)

        return StartD, InstrD, AprenD
    except:
        pass

def split_date(atrr):
    yearx = date.strftime(atrr, '%Y')
    monthx = date.strftime(atrr, '%m')
    dayx = date.strftime(atrr, '%d')
    hourx = date.strftime(atrr, '%H')
    minutx = date.strftime(atrr, '%M')
    secx = date.strftime(atrr, '%S')

    pieceD = [yearx, monthx, dayx, hourx, minutx, secx]

    return pieceD


def start():
    startD, InstrD, AprenD = setup()
    scheduler = BackgroundScheduler()

    scheduler.add_job(noJobSchedule, 'interval', hours = 1)
    #scheduler.add_job(noJobSchedule, 'interval', seconds = 5)

    scheduler.add_job(sendMailInstructores, 'date', run_date=datetime(int(startD[0]), int(startD[1]), int(startD[2]), int(startD[3]), int(startD[4]), int(startD[5])))

    scheduler.add_job(sendMailAprendices, 'date', run_date=datetime(int(InstrD[0]), int(InstrD[1]), int(InstrD[2]), int(InstrD[3]), int(InstrD[4]), int(InstrD[5])))

    scheduler.start()
