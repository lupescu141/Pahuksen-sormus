import random
import mysql.connector
from mysql.connector import errorcode
import random
import keyboard
import random


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

#Listat



#Oliot
class Pelaaja:
    def __init__(self,peli_id,pelaaja_nimi,pelaaja_sijainti, menneet_paivat,pelaaja_hp,pelaaja_suojaus,pelaaja_isku,pelaaja_taitopiste):
        self.id = peli_id
        self.nimi = pelaaja_nimi
        self.sijainti = pelaaja_sijainti
        self.menneet_paivat = menneet_paivat
        self.hp = pelaaja_hp
        self.suojaus = pelaaja_suojaus
        self.isku = pelaaja_isku
        self.taitopiste = pelaaja_taitopiste

    inventaario = []


class Vihollinen:
    def __init__(self, vihollinen_id, vihollinen_nimi, vihollinen_hp, vihollinen_suojaus, vihollinen_isku):
        self.id = vihollinen_id
        self.nimi = vihollinen_nimi
        self.hp = vihollinen_hp
        self.suojaus = vihollinen_suojaus
        self.isku = vihollinen_isku


#FUNKTIOT:

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
            Pelaaja = luo_pelaaja(lataa_peli())
            break

        if keyboard.is_pressed("3"):
            poistu()
            break

    return pelaaja

#Tämä luo uuden tallennuksen tietokantaan eli uuden pelin
def luo_peli():

    while True:
        nimi = input('Anna hahmollesi nimi: ')

        if len(nimi) < 0:
            print('Et voi antaa tyhjää nimeä.')

        elif len(nimi) > 12:
            print('Nimen maksimipituus on 12 merkkiä pitkä')

        else:
            break

    sql = 'INSERT INTO peli (pelaaja_nimi)'
    sql += f"VALUE ('{nimi}');"
    kursori = yhteys.cursor()
    kursori.execute(sql)

    sql = f'SELECT peli_id FROM peli WHERE pelaaja_nimi = "{nimi}";'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    pelaajan_id_sanakirja = kursori.fetchone()
    pelaajan_id = pelaajan_id_sanakirja['peli_id']
    return pelaajan_id

#Hakee viholliset tietokannasta
def hae_viholliset():

    sql = 'select * from viholliset'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    haku_tiedot = kursori.fetchone()
    vihollinen = Vihollinen(haku_tiedot['vihollinen_id'], haku_tiedot['vihollinen_nimi'], haku_tiedot['vihollinen_hp'], haku_tiedot['vihollinen_suojaus'], haku_tiedot['vihollinen_isku'])
    return vihollinen

def luo_pelaaja(peli_id):
    sql = f'SELECT * FROM peli WHERE peli_id = "{peli_id}"'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    haku_tiedot = kursori.fetchone()
    pelaaja = Pelaaja(haku_tiedot['peli_id'], haku_tiedot['pelaaja_nimi'], haku_tiedot['pelaaja_sijainti'], haku_tiedot['menneet_paivat'],
                      haku_tiedot['pelaaja_hp'], haku_tiedot['pelaaja_suojaus'], haku_tiedot['pelaaja_isku'], haku_tiedot['pelaaja_taitopiste'])

    return pelaaja

#Lataa tallennuksen
def lataa_peli():
    sql = 'SELECT peli_id, pelaaja_nimi FROM peli '
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    tallennetut_pelit = kursori.fetchall()

    for tallennus in tallennetut_pelit:
        print(f"{tallennus['peli_id']}. {tallennus['pelaaja_nimi']}")


    while True:
        valinta = input('Mitä tallennusta haluat jatkaa? Kirjoita numero:  ')
        tallennus_haku = False
        for tallennus in tallennetut_pelit:

            if valinta == str(tallennus['peli_id']):
                tallennus_haku = True
                print(f'{valinta} valittu.')
                break

        if tallennus_haku == True:
            break

        print(f"Ei löydy tallennusta valinnalla!")

    return valinta

#Poistuu pelistä
def poistu():
    return

pelaaja = paavalikko()
print(pelaaja.nimi, pelaaja.hp)
pelaaja.hp - 10
print(pelaaja.hp)


def taistelu_mahdollisuus_laskuri(matkan_paivat):
    heitto = random.randint(1, 20)
    if heitto + matkan_paivat > 12:
        return True
    elif heitto + matkan_paivat <= 12:
        return False
    