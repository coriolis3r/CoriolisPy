import sqlite3
import numpy as np

'''
try:
    conn = sqlite3.connect('dataMeter.sqlite')
    dataR = conn.execute("Select MeterName, Address from Meters")

    dr = []
    dr1 = []
    dr2 = []

    for item in dataR:
        dr1.append(item[0])
        dr2.append(item[1])

    conn.close()

    d = np.array(dr1)

    d1 = d[0]

    print(d1)

except Exception as e:
    print('Error')
'''


def InsertMeter(meterData):
    try:

        conn = sqlite3.connect('dataMeter.sqlite')

        conn.execute("INSERT INTO Meters (MeterName,Address) \
          VALUES ('Piso 14', 14)")

        conn.commit()

        conn.close()

    except Exception as e:
        print("Exception")

def SelectAllMeters():
    try:
        conn = sqlite3.connect('dataMeter.sqlite')
        dataR = conn.execute("Select MeterName, Address from Meters")

        dr = []
        dr1 = []
        dr2 = []

        for item in dataR:
            dr1.append(item[0])
            dr2.append(item[1])

        conn.close()

        d = np.array(dr1)

        return (dr1, dr2)

    except Exception as e:
        return []