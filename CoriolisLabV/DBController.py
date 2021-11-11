import mysql.connector

try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Admin.15zz,",
      database = "keepylite"
    )

    cursor = db.cursor()

    query = "insert into meterlistening (ListeningIndex, ListeningId, MeterSerial, ListeningDate) values (%s,%s,%s,%s)"

    values = [(0,'76758F7B-B047-4827-3FDD-AD3DF3529424','5360F440-E660-4385-8g','2021-11-10 17:15:00')]

    ## executing the query with values
    cursor.executemany(query, values)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()

    print(cursor.rowcount, "records inserted")

except Exception as e:
    print(e)
