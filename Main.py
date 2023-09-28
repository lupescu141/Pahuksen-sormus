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

#Päävalikon ohjaukseen
def paavalikko():
#Hakee txt tiedoston ja tulostaa päävalikon visuaalisen tekstin
    for x in open(file="paavalikkoTeksti.txt"):
        print(f"        {x}", end="")
#Ottaa vastaan käyttäjän näppäin painalluksen ja toteuttaa tietyn funktion
    while True:

        if keyboard.is_pressed("1"):
            luo_peli()
            break

        if keyboard.is_pressed("2"):
            lataa_peli()
            break

        if keyboard.is_pressed("3"):
            lataa_peli()
            break


#Tämä luo uuden tallennuksen tietokantaan eli uuden pelin
def luo_peli():

    while True:
        nimi = input('Anna hahmollesi nimi: ')

        if len(nimi) < 0:
            print('Et voi antaa tyhjää nimeä.')

        elif len(nimi) > 12:
            print('Maksimi nimi on 12 merkkiä pitkä')

        else:
            break

    sql = 'INSERT INTO peli (pelaaja_nimi)'
    sql += f"VALUE ('{nimi}');"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return

#Hakee viholliset tietokannasta
def hae_viholliset():

    sql = 'select * from viholliset'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    lista = kursori.fetchall()
    return lista

#Lataa tallennuksen
def lataa_peli():
    return

#Poistuu pelistä
def poistu():
    return

luo_peli()