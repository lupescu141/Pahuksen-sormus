import random
import mysql.connector
from mysql.connector import errorcode
import random
import keyboard


#Tietokannan asetukset:
tietokanta = {'user': 'root',
            'password': 'h93cx3et',
            'host': '127.0.0.1',
            'database': 'pahuksen_sormus',
            'raise_on_warnings': True,
            'autocommit': True}


#Tässä yritetään yhdistää tietokantaan ja palautetaan error viesti jos ei pysty
try:
    yhteys = mysql.connector.connect(**tietokanta)

except mysql.connector.errors.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or password is invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")

    else:
        print(err)
else:
    print("Connection: Succesful")


