import requests
import json
import logging
import os
import uuid
import zipfile
from os.path import basename
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

class CloudProcess(object):
    def __init__(self, urlLB, urlMO, urlLF, JsonPath, ZipPath):
        self.urlLB = urlLB
        self.urlMO = urlMO
        self.urlLF = urlLF
        self.h = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Content-Type': 'application/json; charset=utf-8', 'Expires': '-1', 'Access-Control-Allow-Origin': '*'}
        self.Timestamp = str(int(datetime.today().timestamp()))
        self.JsonPath = JsonPath
        self.ZipPath = ZipPath

    def CreateJson(self,ArrayOfMeterListening):
        try:
            #Save data in JSON file
            jsPath = self.JsonPath + self.Timestamp + ".json"
            with open(jsPath, 'w') as fp:
                json.dump(ArrayOfMeterListening, fp)
        except Exception as e:
            logging.info("Error creating JSON file: %s, %s" %(e,datetime.today()))

    def CreateZipFiles(self):
        try:
            cont = 0
            #Read all json files from JsonFiles directory
            lf = os.listdir(self.JsonPath)

            zfn = str(uuid.uuid4()) + ".zip"

            for fn in lf:
                zn = self.ZipPath + zfn
                z = zipfile.ZipFile(zn, "a")
                jfn = self.JsonPath + fn
                z.write(jfn, basename(jfn))
                z.close()
                #Remove file saved on JSON folder
                os.remove(jfn)
                cont = cont + 1
                if cont >= 100:
                    zfn = str(uuid.uuid4()) + ".zip"
                    cont = 0

        except Exception as e:
            logging.info("Error CreateZipFiles: %s, %s" %(e,datetime.today()))

    def SendDataCloud(self,ArrayOfMeterListening):
        try:
            #requests.post(url='https://localhost:44335/api/ProcessData/PostMeterListeningL', data=None, json=data, verify=False)
            r = requests.post(url = self.urlLB, data = None, json = ArrayOfMeterListening, verify = False)
            if r.status_code != 200:
                self.CreateJson(ArrayOfMeterListening)

        except Exception as e:
            logging.info("Error SendDataCloud: %s, %s" %(e,datetime.today()))
            self.CreateJson(ArrayOfMeterListening)

    def SendZipFiles(self):
        try:

            cntTry = 0

            while cntTry < 5:

                lzf = os.listdir(self.ZipPath)[:10]

                if len(lzf) > 0:
                    for lz in lzf:
                        f = {'file': open(self.ZipPath + lz, 'rb')}
                        r = requests.post(self.urlLF, files = f)
                        f = None
                        if r.status_code == 200:
                            os.remove(self.ZipPath + lz)
                        else:
                            cntTry += 1
                else:
                    cntTry = 10

        except Exception as e:
            logging.info("Error SendZipFiles: %s, %s" %(e,datetime.today()))
