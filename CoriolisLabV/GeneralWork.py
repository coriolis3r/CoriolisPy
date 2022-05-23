import logging
from datetime import datetime
import json
import mysql.connector
import numpy as np

def MainWork(mainPath):

    URLArr = []

    csPath = mainPath + '/CloudService.log'

    logging.basicConfig(filename=csPath, level=logging.INFO)

    logging.info("Starting... %s" % (datetime.today()))
    # time.sleep(max(0, 60-(time.time() % 60)))
    logging.info("Started... %s" % (datetime.today()))

    ConfigFilesPath = mainPath + '/ConfigFiles/'

    # Get URL and  folders path
    logging.info("Loading URL and  folders path... %s" % (datetime.today()))
    with open(ConfigFilesPath + 'URLs.json') as f:
        URLs = json.loads(f.read())

    URLArr.append(URLs[0]["urlLB"])
    URLArr.append(URLs[0]["urlMO"])
    URLArr.append(URLs[0]["urlLF"])

    return URLArr

def GetData():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin.15zz,",
            database="CoriolisDB"
        )

        cursor = db.cursor()

        query = "insert into meterlistening (ListeningIndex, ListeningId, MeterSerial, ListeningDate) values (%s,%s,%s,%s)"
        query1 = "select ParameterID, Value from listeningvalues where ListeningID = %s"
        tuple = ('00095745-04BE-4A0F-80C1-EFB37F99B642',)

        values = [(0, '76758F7B-B047-4827-3FDD-AD3DF3529424', '5360F440-E660-4385-8g', '2021-11-10 17:15:00')]

        ## executing the query with values
        # data = cursor.executemany(query, values)
        cursor.execute(query1, tuple)

        data1 = cursor.fetchall()

        dataArr = []

        for vr in data1:
            dataArr1 = [vr[0], vr[1]]
            dataArr.append(dataArr1)

        db.commit()

        return dataArr

    except Exception as e:
        print(e)

def GetDataSP(mainPath):
    try:
        dbData = []
        csPath = mainPath + '/CloudService.log'

        logging.basicConfig(filename=csPath, level=logging.INFO)

        ConfigConnection = mainPath + '/ConfigFiles/'

        with open(ConfigConnection + 'DBConnection.json') as f:
            ConnData = json.loads(f.read())

        db = mysql.connector.connect(
            host=ConnData[0]["host"],
            user=ConnData[0]["user"],
            password=ConnData[0]["password"],
            database=ConnData[0]["database"],
            port=ConnData[0]["port"]
        )

        cursor = db.cursor()

        args = [1, '2022-05-16', 3, ]

        cursor.callproc('GeneralTrendData', args)

        data = []

        for result in cursor.stored_results():
            data.append(result.fetchall())

        data1 = data[0]
        data2 = data[1]

        dspr = np.array(data1)
        dspr1 = np.array(data2)

        db.commit()

        return (dspr,dspr1)

    except Exception as e:
        print(e)

def TestMult():
    a=[(1,2.5),(3,4.2)]
    b=np.array(a)
    return b

def returnmultiple():
    return (['a','b','c'],([(1,2),(2,3)],True))

def retTuple():
    return ([[1,2,5.5],[3,4,3.6]],[[5,6],[7,8]])

def passdict(keys,values):
    adict=dict(zip(keys,values))
    return (list(adict.keys()),list(adict.values()))

def editlist(alist,anum,astr,nestedlist):
    alist.append(5)
    anum += 1
    astr += 'Python'
    nestedlist[0].append(5)
    return