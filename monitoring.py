"""
Monitoring mysql database via listing publisher URL
"""

import time
from subprocess import call
import mysql.connector

try:
    # MySql Connection config
    mydb = mysql.connector.connect(
        host="",
        user="",
        passwd="",
        database=""
    )

    cursor = mydb.cursor()
    sql = "SELECT publisherUrl, platform FROM monitoring"
    cursor.execute(sql)
    resultSet = cursor.fetchall()
    print(resultSet)
    for row in resultSet:
        publisherUrlFromDb = row[0]
        publisherPlatformFromDb = row[1]

        # Scan and store the data
        call('python3.6 scanner-webpagetest.py '+publisherUrlFromDb+' '+publisherPlatformFromDb, shell=True)

        # Waiting for 5 seconds to get refreshed.
        time.sleep(5)

except Exception as e:
    print("Something went wrong while running monitoring")