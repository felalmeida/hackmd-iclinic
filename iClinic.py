#!/usr/bin/python3
# -*- coding: UTF-8 -*-
###############################################################################
# Module:   iClinic.py                 Autor: Felipe Almeida                  #
# Start:    06-Ago-2019                Last Update: 07-Ago-2019  Version: 1.0 #
###############################################################################

import sys
import requests
import json
import threading
import pymongo
from datetime import datetime
from flask import Flask, request

iClinicPostApp = Flask(__name__)
iClinicPostPath = "/v2/prescriptions"
iClinicPostPort = 5000

MongoObj = pymongo.MongoClient('172.17.0.2', 27017)
MongoDB = MongoObj.iclinic_db

Errors = {
    "01": "malformed request",
    "02": "physician not found",
    "03": "patient not found",
    "04": "metrics service not available",
    "05": "physicians service not available",
    "06": "patients service not available",
    "07": "physicians service timeout",
    "08": "patients service timeout",
    "09": "clinic not found",
    "10": "clinic service not available",
    "11": "clinic service timeout",
    "12": "malformed request (clinic)",
    "13": "malformed request (physician)",
    "14": "malformed request (patient)",
    "15": "malformed request (text)",
    "16": "metrics service timeout"
}

jPhysician = ""
jClinic = ""
jPatient = ""
nRequestId = 0


def GetPhysicianAPI(v_PhysicianId=-1):
    global jPhysician, Errors

    PhysicianHost = "https://cryptic-scrubland-98389.herokuapp.com"
    PhysicianMethod = "GET"
    PhysicianPath = "/v2/physicians/"
    PhysicianTimeOut = 4
    PhysicianRetry = 2
    PhysicianAuth = ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW" +
                     "IiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF" +
                     "0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9" +
                     ".Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA")
    PhysicianUrl = PhysicianHost + PhysicianPath + str(v_PhysicianId)

    Head = {
        'Authorization': PhysicianAuth,
        'User-Agent': "Mozilla/5.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': PhysicianHost[8:],
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    GetAPIStatus = False
    GetAPIRun = 0
    jResponse = ""

    while ((not GetAPIStatus) and (GetAPIRun < PhysicianRetry)):
        GetAPIRun = GetAPIRun + 1
        try:
            Response = requests.request(PhysicianMethod, PhysicianUrl,
                                        headers=Head, timeout=PhysicianTimeOut)
            if (Response.status_code == 200):
                GetAPIStatus = True
            jResponse = json.loads(Response.text)
        except requests.exceptions.Timeout:
            jErrorStr = ('{"error":{"message":"'+Errors['07']+'","code":"07"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)
        except:
            jErrorStr = ('{"error":{"message":"'+Errors['05']+'","code":"05"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)

    if ('errorCode' in jResponse):
        if (int(jResponse['errorCode']) == 4040):
            jErrorStr = '{"error":{"message":"'+Errors['02']+'","code":"02"}}'
        else:
            jErrorStr = ('{"error":{"message":"'+jResponse['userMessage'] +
                         '","code":"'+jResponse['errorCode']+'"}}')
        jResponse = json.loads(jErrorStr)

    jPhysician = jResponse


def GetClinicAPI(v_ClinicId=-1):
    global jClinic, Errors

    ClinicHost = "https://agile-earth-43435.herokuapp.com"
    ClinicMethod = "GET"
    ClinicPath = "/v1/clinics/"
    ClinicTimeOut = 5
    ClinicRetry = 3
    ClinicAuth = ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi" +
                  "IxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE" +
                  "2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhO" +
                  "UK8YnIdLhVGJEqnReSClLCMBIJRQ")
    ClinicUrl = ClinicHost + ClinicPath + str(v_ClinicId)

    Head = {
        'User-Agent': "Mozilla/5.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': ClinicHost[8:],
        'Authorization': ClinicAuth,
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    GetAPIStatus = False
    GetAPIRun = 0
    jResponse = ""

    while ((not GetAPIStatus) and (GetAPIRun < ClinicRetry)):
        GetAPIRun = GetAPIRun + 1
        try:
            Response = requests.request(ClinicMethod, ClinicUrl,
                                        headers=Head, timeout=ClinicTimeOut)
            if (Response.status_code == 200):
                GetAPIStatus = True
            jResponse = json.loads(Response.text)
        except requests.exceptions.Timeout:
            jErrorStr = ('{"error":{"message":"'+Errors['11']+'","code":"11"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)
        except:
            jErrorStr = ('{"error":{"message":"'+Errors['10']+'","code":"10"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)

    if ('errorCode' in jResponse):
        if (int(jResponse['errorCode']) == 4040):
            jErrorStr = '{"error":{"message":"'+Errors['09']+'","code":"09"}}'
        else:
            jErrorStr = ('{"error":{"message":"'+jResponse['userMessage'] +
                         '","code":"'+jResponse['errorCode']+'"}}')
        jResponse = json.loads(jErrorStr)

    jClinic = jResponse


def GetPatientAPI(v_PatientId=-1):
    global jPatient, Errors

    PatientHost = "https://limitless-shore-81569.herokuapp.com"
    PatientMethod = "GET"
    PatientPath = "/v3/patients/"
    PatientTimeOut = 3
    PatientRetry = 2
    PatientAuth = ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi" +
                   "IxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE" +
                   "2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX" +
                   "8Y09hEBzl7dluxsGiaxGlfzdaphzVU")
    PatientUrl = PatientHost + PatientPath + str(v_PatientId)

    Head = {
        'User-Agent': "Mozilla/5.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': PatientHost[8:],
        'Authorization': PatientAuth,
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    GetAPIStatus = False
    GetAPIRun = 0
    jResponse = ""

    while ((not GetAPIStatus) and (GetAPIRun < PatientRetry)):
        GetAPIRun = GetAPIRun + 1
        try:
            Response = requests.request(PatientMethod, PatientUrl,
                                        headers=Head, timeout=PatientTimeOut)
            if (Response.status_code == 200):
                GetAPIStatus = True
            jResponse = json.loads(Response.text)
        except requests.exceptions.Timeout:
            jErrorStr = ('{"error":{"message":"'+Errors['08']+'","code":"08"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)
        except:
            jErrorStr = ('{"error":{"message":"'+Errors['06']+'","code":"06"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)

    if ('errorCode' in jResponse):
        if (int(jResponse['errorCode']) == 4040):
            jErrorStr = '{"error":{"message":"'+Errors['03']+'","code":"03"}}'
        else:
            jErrorStr = ('{"error":{"message":"'+jResponse['userMessage'] +
                         '","code":"'+jResponse['errorCode']+'"}}')
        jResponse = json.loads(jErrorStr)

    jPatient = jResponse


def SetMetricsAPI(v_jMetrics):
    global Errors

    MetricsHost = "https://mysterious-island-73235.herokuapp.com"
    MetricsMethod = "POST"
    MetricsPath = "/api/metrics"
    MetricsTimeOut = 6
    MetricsRetry = 5
    MetricsAuth = ("Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    MetricsUrl = MetricsHost + MetricsPath

    Head = {
        'User-Agent': "Mozilla/5.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': MetricsHost[8:],
        'Authorization': MetricsAuth,
        'Content-Type': "application/json",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    GetAPIStatus = False
    GetAPIRun = 0
    jResponse = ""

    while ((not GetAPIStatus) and (GetAPIRun < MetricsRetry)):
        GetAPIRun = GetAPIRun + 1
        try:
            Response = requests.request(MetricsMethod, MetricsUrl,
                                        headers=Head, timeout=MetricsTimeOut,
                                        data=v_jMetrics)
            if (Response.status_code == 200):
                GetAPIStatus = True
            jResponse = json.loads(Response.text)
        except requests.exceptions.Timeout:
            jErrorStr = ('{"error":{"message":"'+Errors['16']+'","code":"16"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)
        except:
            jErrorStr = ('{"error":{"message":"'+Errors['04']+'","code":"04"' +
                         ',"retries":'+str(GetAPIRun)+'}}')
            jResponse = json.loads(jErrorStr)

    if ('errorCode' in jResponse):
        jErrorStr = ('{"error":{"message":"'+jResponse['userMessage'] +
                     '","code":"'+jResponse['errorCode']+'"}}')
        jResponse = json.loads(jErrorStr)

    return jResponse


def GetPhysician(v_PhysicianId=-1):
    global jPhysician, MongoDB

    PhysicianTTL = (48*3600)
    MongoAlb = MongoDB.iclinic_physician_collection

    PhysicianDB = (MongoAlb.find_one({"_id": v_PhysicianId}))
    if (PhysicianDB is not None):
        DbTTL = int(datetime.utcnow().timestamp()) - PhysicianDB['insert_ts']
        if (DbTTL > PhysicianTTL):
            GetPhysicianAPI(v_PhysicianId)
            MongoAlb.delete_one({"_id": v_PhysicianId})
            jPhysician['_id'] = jPhysician['data']['id']
            jPhysician['insert_ts'] = int(datetime.utcnow().timestamp())
            MongoAlb.insert_one(jPhysician)
        else:
            print("Returning Physician from MongoDB")
            jPhysician = PhysicianDB
    else:
        GetPhysicianAPI(v_PhysicianId)
        if ('error' not in jPhysician):
            jPhysician['_id'] = jPhysician['data']['id']
            jPhysician['insert_ts'] = int(datetime.utcnow().timestamp())
            MongoAlb.insert_one(jPhysician)


def GetClinic(v_ClinicId=-1):
    global jClinic, MongoDB

    ClinicTTL = (72*3600)
    MongoAlb = MongoDB.iclinic_clinic_collection

    ClinicDB = (MongoAlb.find_one({"_id": v_ClinicId}))
    if (ClinicDB is not None):
        DbTTL = int(datetime.utcnow().timestamp()) - ClinicDB['insert_ts']
        if (DbTTL > ClinicTTL):
            GetClinicAPI(v_ClinicId)
            MongoAlb.delete_one({"_id": v_ClinicId})
            jClinic['_id'] = jClinic['data']['id']
            jClinic['insert_ts'] = int(datetime.utcnow().timestamp())
            MongoAlb.insert_one(jClinic)
        else:
            print("Returning Clinic from MongoDB")
            jClinic = ClinicDB
    else:
        GetClinicAPI(v_ClinicId)
        if ('error' not in jClinic):
            jClinic['_id'] = jClinic['data']['id']
            jClinic['insert_ts'] = int(datetime.utcnow().timestamp())
            MongoAlb.insert_one(jClinic)


def GetPatient(v_PatientId=-1):
    global jPatient, MongoDB

    PatientTTL = (12*3600)
    MongoAlb = MongoDB.iclinic_patient_collection

    PatientDB = (MongoAlb.find_one({"_id": v_PatientId}))
    if (PatientDB is not None):
        DbTTL = int(datetime.utcnow().timestamp()) - PatientDB['insert_ts']
        if (DbTTL > PatientTTL):
            GetPatientAPI(v_PatientId)
            MongoAlb.delete_one({"_id": v_PatientId})
            jPatient['_id'] = jPatient['data']['id']
            jPatient['insert_ts'] = int(datetime.utcnow().timestamp())
            MongoAlb.insert_one(jPatient)
        else:
            print("Returning Patient from MongoDB")
            jPatient = PatientDB
    else:
        GetPatientAPI(v_PatientId)
        if ('error' not in jPatient):
            jPatient['_id'] = jPatient['data']['id']
            jPatient['insert_ts'] = int(datetime.utcnow().timestamp())
            MongoAlb.insert_one(jPatient)


def ProcessPost(v_PostJson=""):
    global jPhysician, jClinic, jPatient, nRequestId

    pPhysicianId = v_PostJson['physician']['id']
    pClinicId = v_PostJson['clinic']['id']
    pPatientId = v_PostJson['patient']['id']
    pText = v_PostJson['text']

    '''
    Create Threads for Async Request in the APIs
    '''
    tPhysician = threading.Thread(target=GetPhysician, args=(pPhysicianId, ))
    tPhysician.start()

    tClinic = threading.Thread(target=GetClinic, args=(pClinicId, ))
    tClinic.start()

    tPatient = threading.Thread(target=GetPatient, args=(pPatientId, ))
    tPatient.start()

    '''
    Get the returns of all APIs
    '''
    tPhysician.join()
    tClinic.join()
    tPatient.join()

    if ('error' in jPhysician):
        return json.dumps(jPhysician, indent=4, sort_keys=True)
    if ('error' in jPatient):
        return json.dumps(jPatient, indent=4, sort_keys=True)
    # if ('error' in jClinic):
    #     return json.dumps(jClinic, indent=4, sort_keys=True)

    '''
    Create Metrics Request Body
    '''

    '''
    Ignore Errors in Clinic API
    '''
    if ('error' in jClinic):
        dMetrics = {
            'physician_id':     jPhysician['data']['id'],
            'physician_name':   jPhysician['data']['fullName'],
            'physician_crm':    jPhysician['data']['crm'],
            'patient_id':       jPatient['data']['id'],
            'patient_name':     jPatient['data']['fullName'],
            'patient_email':    jPatient['data']['email'],
            'patient_phone':    jPatient['data']['phone']
        }
    else:
        dMetrics = {
            'clinic_id':        jClinic['data']['id'],
            'clinic_name':      jClinic['data']['name'],
            'physician_id':     jPhysician['data']['id'],
            'physician_name':   jPhysician['data']['fullName'],
            'physician_crm':    jPhysician['data']['crm'],
            'patient_id':       jPatient['data']['id'],
            'patient_name':     jPatient['data']['fullName'],
            'patient_email':    jPatient['data']['email'],
            'patient_phone':    jPatient['data']['phone']
        }
    jMetricsReturn = SetMetricsAPI(json.dumps(dMetrics))
    if ('error' in jMetricsReturn):
        return json.dumps(jMetricsReturn, indent=4, sort_keys=True)

    '''
    Response Json
    '''
    dResponse = {
        'data': {
            'id': nRequestId,
            'clinic': {
                'id': pClinicId
            },
            'physician': {
                'id': pPhysicianId
            },
            'patient': {
                'id': pPatientId
            },
            'text': pText
        }
    }
    return json.dumps(dResponse, indent=4, sort_keys=True)


@iClinicPostApp.route(iClinicPostPath, methods=['POST'])
def PostApp():
    global nRequestId, Errors

    nRequestId = nRequestId + 1

    jPost = ""
    jErrorStr = ""
    PostStatus = False
    JsonStatus = False

    jClinicErrorStr = '{"error":{"message":"'+Errors['12']+'","code":"12"}}'
    jPhysicianErrorStr = '{"error":{"message":"'+Errors['13']+'","code":"13"}}'
    jPatientErrorStr = '{"error":{"message":"'+Errors['14']+'","code":"14"}}'
    jTextErrorStr = '{"error":{"message":"'+Errors['15']+'","code":"15"}}'

    try:
        jPost = json.loads(request.data)
        PostStatus = True
    except:
        jErrorStr = '{"error":{"message":"'+Errors['01']+'","code":"01"}}'

    if (PostStatus):
        if ('clinic' in jPost):
            if ('id' in jPost['clinic']):
                JsonStatus = True
            else:
                jErrorStr = jClinicErrorStr
        else:
            jErrorStr = jClinicErrorStr

        if ('physician' in jPost):
            if ('id' in jPost['physician']):
                JsonStatus = JsonStatus and True
            else:
                jErrorStr = jPhysicianErrorStr
                JsonStatus = False
        else:
            jErrorStr = jPhysicianErrorStr
            JsonStatus = False

        if ('patient' in jPost):
            if ('id' in jPost['patient']):
                JsonStatus = JsonStatus and True
            else:
                jErrorStr = jPatientErrorStr
                JsonStatus = False
        else:
            jErrorStr = jPatientErrorStr
            JsonStatus = False

        if ('text' in jPost):
            JsonStatus = JsonStatus and True
        else:
            jErrorStr = jTextErrorStr
            JsonStatus = False

    if ((not PostStatus) or (not JsonStatus)):
        jPost = json.loads(jErrorStr)
        return json.dumps(jPost, indent=4, sort_keys=True)
    else:
        return ProcessPost(jPost)


def MainProcess():
    global iClinicPostApp, iClinicPostPort
    iClinicPostApp.run(port=iClinicPostPort)


def main():
    try:
        MainProcess()
        sys.exit(0)
    except KeyboardInterrupt:
        print("iClinic Challenge Interrupted!")
        sys.exit(1)


if __name__ == "__main__":
    main()
