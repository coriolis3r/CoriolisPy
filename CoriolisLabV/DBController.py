import mysql.connector
import numpy as np

try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Admin.15zz,",
      database = "keepylite"
    )

    cursor = db.cursor()

    query = "insert into meterlistening (ListeningIndex, ListeningId, MeterSerial, ListeningDate) values (%s,%s,%s,%s)"
    query1 = "select ParameterID,Value from listeningvalues where ListeningID = %s"
    tuple = ('00095745-04BE-4A0F-80C1-EFB37F99B642',)

    values = [(0,'76758F7B-B047-4827-3FDD-AD3DF3529424','5360F440-E660-4385-8g','2021-11-10 17:15:00')]

    ## executing the query with values
    #data = cursor.executemany(query, values)
    cursor.execute(query1,tuple)

    data1 = cursor.fetchall()
    dataArr = []

    for vr in data1:
        dataArr1 = [vr[0],vr[1]]
        dataArr.append(dataArr1)

    for vr in data1:
        print(vr)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()

    print(cursor.rowcount, "records inserted")

except Exception as e:
    print(e)