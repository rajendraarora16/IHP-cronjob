"""
Python - slack bot to check loader.js performance in by
vising to
"""
import json
import sys
from datetime import datetime
from subprocess import call

import mysql.connector
import requests

try:
    publisher_arg_url = sys.argv[1]
    publisher_arg_platform = sys.argv[2]

except:
    sys.exit("You have not passed the url")

"""
Getting the response from Taboola monitoring website
"""
try:

    # MySql Connection config
    mydb = mysql.connector.connect(
        host="",
        user="",
        passwd="",
        database=""
    )

    taboola_monitor_url = '<domain>/runtest.php'

    if (publisher_arg_platform == 'PHON'):
        # Mobile
        # Config to test web page.
        params = dict(
            url=publisher_arg_url,
            f='json',
            mobile=1,
            mobileDevice='Nexus5',
            runs=1,
            bwDown=5000,
            bwUp=1000,
            latency=28,
            timeline=1,
            platform=publisher_arg_platform
        )
    else:
        # Desktop
        # Config to test web page.
        params = dict(
            url=publisher_arg_url,
            f='json',
            runs=1,
            bwDown=5000,
            bwUp=1000,
            latency=28,
            timeline=1,
            platform=publisher_arg_platform
        )

    resp = requests.get(taboola_monitor_url, params)
    taboola_monitor_data = json.loads(json.dumps(resp.json()))

    # Status of the response
    statusCode = taboola_monitor_data["statusCode"]

    if statusCode == 200:
        isErrorStr = "false"
    else:
        isErrorStr = "true"

    ##
    ## Parsing Taboola monitoring values
    ##
    testId = taboola_monitor_data["data"]["testId"]
    jsonUrl = taboola_monitor_data["data"]["jsonUrl"]
    webTestingUrlConf = str(params)
    summaryUrl = "<domain>/results.php?test=" + testId
    platform = publisher_arg_platform
    createdAt = datetime.now().strftime("%Y-%m-%d %H:%M%p ")

    mycursor = mydb.cursor()

    # Insert the data in mysql database
    sql = "INSERT INTO logger_web_page(testId, jsonUrl, webTestingUrlConf, summaryUrl, platform, createdAt, isError) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (testId, jsonUrl, webTestingUrlConf, summaryUrl, platform, createdAt, isErrorStr)

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")

except Exception as e:
    print('Something went wrong: ' + str(e))
