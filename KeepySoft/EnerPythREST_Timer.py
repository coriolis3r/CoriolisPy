import time
import logging
from DataProcessCloud import *
from SendDataREST import *
from datetime import datetime
import json
import RPi.GPIO as GPIO

try:

    cntEnvData = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(27, GPIO.OUT)

    GPIO.output(27, GPIO.LOW)

    mainPath = '/home/pi/Keepyware/'
    #mainPath = './'
    #mainPath = '/root/Keepyware/'
    csPath = mainPath + 'CloudService.log'

    logging.basicConfig(filename=csPath,level=logging.INFO)

    logging.info("Starting... %s" %(datetime.today()))
    time.sleep(max(0, 60-(time.time() % 60)))
    logging.info("Started... %s" %(datetime.today()))

    ConfigFilesPath = mainPath + 'ConfigFiles/'
    MBMetersFiles = mainPath + 'MB_Meters/'
    JsonPath = mainPath + 'JsonFiles/'
    ZipPath = mainPath + 'ZipFiles/'

    JsonMeters = []
    prName = 'Meter1'
    acName = 'Meter2'

    # Get URL and  folders path
    logging.info("Loading URLs... %s" % (datetime.today()))
    with open(ConfigFilesPath + 'URLs.json') as f:
        URLs = json.loads(f.read())

    urlLB = URLs[0]["urlLB"]
    urlMO = URLs[0]["urlMO"]
    urlLF = URLs[0]["urlLF"]

    # Get serial port configuration
    logging.info("Loading Serial Configuration... %s" %(datetime.today()))
    with open(ConfigFilesPath + 'SerialPort.json') as f:
        SerialPort = json.loads(f.read())

    #Get general configuration
    logging.info("Loading General Configuration... %s" %(datetime.today()))
    with open(ConfigFilesPath + 'MeterConfig.json') as f:
        MeterConfig = json.loads(f.read())

    # Get MB map for all devices connected
    logging.info("Loading MB configuration... %s" %(datetime.today()))
    for mc in MeterConfig:
         if mc["ConStatus"]:
             acName = mc["Models"]["ModelName"]
             if(acName != prName):
                 with open(MBMetersFiles + mc["Models"]["ModelName"] + '.json') as f:
                     JsonMeters.append(json.loads(f.read()))
             prName = acName

    # Get URL for FTP files
    logging.info("Loading FTP data... %s" % (datetime.today()))
    with open(ConfigFilesPath + 'FTP_access.json') as f:
        FTP_access = json.loads(f.read())

    #Init class CloudProcess
    sdr = CloudProcess(urlLB, urlMO, urlLF, JsonPath, ZipPath, FTP_access)
    #init class ReadAllMeters
    mbp = DataProcessCloud()

    time.sleep(max(0, 60-(time.time() % 60)))

    #Main Process
    logging.info("Running main process... %s" %(datetime.today()))

    #Try send ZIP data to DB
    try:
        sdr.SendZipFiles()
    except Exception as e:
        logging.info("Error sending initial ZIP files to server: %s, %s" % (e, datetime.today()))

    while True:
        try:
            logging.basicConfig(filename=csPath, level=logging.INFO)

            dt = datetime.today()

            mlv = mbp.ReadAllMeters(SerialPort, MeterConfig, JsonMeters)

            if mlv:
                sdr.SendDataCloud(mlv)

            if (dt.minute % 1) == 0:
                cntEnvData += 1

            if (cntEnvData > 30):
                sdr.CreateZipFiles()
                sdr.SendZipFiles()
                cntEnvData = 0

            time.sleep(max(0, 60-(time.time() % 60)))


        except Exception as e:
            logging.info("General error: %s, %s" %(e, datetime.today()))
            time.sleep(max(0, 60-(time.time() % 60)))

        finally:
            GPIO.output(27, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(27, GPIO.LOW)

except Exception as e: 
    logging.info("Application can't be started: %s, %s" %(e, datetime.today()))