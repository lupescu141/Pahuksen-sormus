from colorama import Fore
from colorama import Style
import geopy
from geopy import distance
import mysql.connector
from mysql.connector import errorcode
import keyboard
import random
import winsound
import sys
import time

# Tietokannan asetukset:

tietokanta = {'user': 'root',
              'password': 'h93cx3et',
              'host': '127.0.0.1',
              'database': 'pahuksen_sormus',
              'raise_on_warnings': True,
              'autocommit': True}

# Tässä yritetään yhdistää tietokantaan ja palautetaan error viesti jos syntyy virhe

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
    print("Connection: Successful")


# OLIOT:
class Pelaaja:
    def __init__(self, peli_id, pelaaja_nimi, pelaaja_sijainti, menneet_paivat, pelaaja_hp, pelaaja_maxhp, pelaaja_suojaus,
                 pelaaja_isku, pelaaja_taitopiste, pelaaja_max_taitopiste, onko_sormus):
        self.id = peli_id
        self.nimi = pelaaja_nimi
        self.sijainti = pelaaja_sijainti
        self.menneet_paivat = menneet_paivat
        self.hp = pelaaja_hp
        self.maxhp = pelaaja_maxhp
        self.suojaus = pelaaja_suojaus
        self.isku = pelaaja_isku
        self.taitopiste = pelaaja_taitopiste
        self.max_taitopiste = pelaaja_max_taitopiste
        self.onko_sormus = onko_sormus


class Vihollinen:
    def __init__(self, vihollinen_id, vihollinen_nimi, vihollinen_hp, vihollinen_maxhp, vihollinen_suojaus, vihollinen_isku):
        self.id = vihollinen_id
        self.nimi = vihollinen_nimi
        self.hp = vihollinen_hp
        self.maxhp = vihollinen_maxhp
        self.suojaus = vihollinen_suojaus
        self.isku = vihollinen_isku


# FUNKTIOT:
def hae_kaikki_kohteet(pelaaja):

    sql = f'''SELECT airport.id, airport.fantasia_nimi, airport.latitude_deg, airport.longitude_deg 
              FROM airport WHERE airport.id != {pelaaja.sijainti}'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    lista = kursori.fetchall()
    #for nimi in lista:
        #print(nimi)
    return lista


def hae_random_vihollinen():

    sql = 'SELECT * FROM viholliset ORDER by RAND() LIMIT 1'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    haku_tiedot = kursori.fetchone()
    vihollinen = Vihollinen(haku_tiedot['vihollinen_id'], haku_tiedot['vihollinen_nimi'], haku_tiedot['vihollinen_hp'],
                            haku_tiedot['vihollinen_maksimi_hp'], haku_tiedot['vihollinen_suojaus'],
                            haku_tiedot['vihollinen_isku'])
    return vihollinen


def km_to_day(matka):

    if matka < 50:
        aika = 1
        return aika

    elif matka < 100:
        aika = 2
        return aika

    elif matka < 200:
        aika = 3
        return aika

    else:
        aika = 4
        return aika


# Lisää uuden rivin peli tauluun eli luo uuden tallennuksen ja palauttaa tämän hetkisen tallennuksen id arvon.
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
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)

    sql = f'SELECT peli_id FROM peli WHERE pelaaja_nimi = "{nimi}";'
    kursori.execute(sql)
    pelaajan_id_sanakirja = kursori.fetchone()
    pelaajan_id = pelaajan_id_sanakirja['peli_id']
    return pelaajan_id


# Hakee id perusteella pelaajan hahmon tiedot, sitten luo ja palauttaa pelaaja olion.
def luo_pelaaja(peli_id):

    sql = f'SELECT * FROM peli WHERE peli_id = "{peli_id}"'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    haku_tiedot = kursori.fetchone()
    pelaaja = Pelaaja(haku_tiedot['peli_id'], haku_tiedot['pelaaja_nimi'], haku_tiedot['pelaaja_sijainti'],
                      haku_tiedot['menneet_paivat'], haku_tiedot['pelaaja_hp'], haku_tiedot['pelaaja_maksimi_hp'],
                      haku_tiedot['pelaaja_suojaus'], haku_tiedot['pelaaja_isku'],
                      haku_tiedot['pelaaja_taitopiste'], haku_tiedot['pelaaja_maksimi_taitopiste'], haku_tiedot['onko_sormus'])
    return pelaaja


# Tulostaa käyttäjälle tallennukset ja palauttaa käyttäjän syötteen
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


def sijainti_valitsin(pelaaja):

    id_lista = []
    oikea_kohde = 0

    for kohde in hae_kaikki_kohteet(pelaaja):
        loppu_koordinaatit = kohde['latitude_deg'], kohde['longitude_deg']
        alku_koordinaatit = nykyinen_sijainti['latitude_deg'], nykyinen_sijainti['longitude_deg']
        matka = distance.distance(alku_koordinaatit, loppu_koordinaatit).km

        if matka < 50:
            print(f"{kohde['id']:2}. Kohteeseen {kohde['fantasia_nimi']:28} {km_to_day(matka)} päivän matkustus.")
            id_lista.append(kohde['id'])
        elif matka < 100:
            print(f"{kohde['id']:2}. Kohteeseen {kohde['fantasia_nimi']:28} {km_to_day(matka)} päivän matkustus.")
            id_lista.append(kohde['id'])
        elif matka < 200:
            print(f"{kohde['id']:2}. Kohteeseen {kohde['fantasia_nimi']:28} {km_to_day(matka)} päivän matkustus.")
            id_lista.append(kohde['id'])
        elif matka > 200:
            print(f"{kohde['id']:2}. Kohteeseen {kohde['fantasia_nimi']:28} {km_to_day(matka)} päivän matkustus.")
            id_lista.append(kohde['id'])

    print(f'Olet kohteessa {nykyinen_sijainti["fantasia_nimi"]}')

    while True:

        valinta = input('Mihin kohteeseen haluat matkustaa? Kirjoita numero: ')

        for id in id_lista:

            if str(id) == valinta:
                print(f'{valinta} valittu!')
                oikea_kohde = 1

        if oikea_kohde == 1:
            break

        else:
            print('Virheellinen kohde.')

    return valinta


def paavalikko():

    # Hakee txt tiedoston ja tulostaa päävalikon visuaalisen tekstin
    for x in open(file="paavalikkoTeksti.txt"):
        print(f"        {x}", end="")

    # Ottaa vastaan käyttäjän näppäinpainalluksen ja toteuttaa sen perusteella tietyn funktion
    while True:

        if keyboard.is_pressed("1"):
            pelaaja = luo_pelaaja(luo_peli())
            break

        if keyboard.is_pressed("2"):
            pelaaja = luo_pelaaja(lataa_peli())
            break

        if keyboard.is_pressed("3"):
            poistu()
            break

    return pelaaja

def paivien_lisaaja(haluttu_kohde_id, pelaaja):

    sql = f'''SELECT airport.id, airport.fantasia_nimi, airport.latitude_deg, airport.longitude_deg 
              FROM airport WHERE airport.id = {haluttu_kohde_id}'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    kohde = kursori.fetchone()
    loppu_koordinaatit = kohde['latitude_deg'], kohde['longitude_deg']
    alku_koordinaatit = nykyinen_sijainti['latitude_deg'], nykyinen_sijainti['longitude_deg']
    matka = distance.distance(alku_koordinaatit, loppu_koordinaatit).km
    pelaaja.menneet_paivat = int(pelaaja.menneet_paivat) + int(km_to_day(matka))
    pelaaja.sijainti = int(kohde["id"])

    #testauksen vuoksi tulostus
    print(f'Pelaajaolion sijainti on {pelaaja.sijainti}')
    print(f'Pelaajaolion käytetyt päivät ovat {pelaaja.menneet_paivat}')

    return km_to_day(matka)

# Sulkee ohjelman
def poistu():

    sys.exit(0)


# Palauttaa sijainnin tiedot airport taulusta pelaajan sijainnin perusteella
def pelaajan_sijainti(peli_id):

    sql = f'''SELECT airport.id, airport.fantasia_nimi, airport.latitude_deg, airport.longitude_deg
              FROM peli, airport
              WHERE airport.id = peli.pelaaja_sijainti and peli_id = "{peli_id}"'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    tiedot = kursori.fetchone()
    #print(tiedot)
    return tiedot


# Arpoo sormuksen sijainnin peli tauluun
def sormus_arpominen():

    sql = f'''SELECT airport.id FROM airport 
              WHERE airport.fantasia_nimi != 'Uudentoivon-Kylä' 
              AND airport.fantasia_nimi != 'Tulivuori'
              ORDER BY RAND()
              LIMIT 1;'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    sijainti_id = kursori.fetchone()

    sql = f'''UPDATE peli SET sormus_sijainti = {sijainti_id['id']}
              WHERE peli_id = "{pelaaja.id}"'''
    kursori.execute(sql)
    #print('Testaamisen vuoksi:')
    #print('sormuksen random sijainti on ' + str(sijainti_id['id']))
    return sijainti_id['id']


# Tulostaa taistelu valikon ja ohjaa taistelua
def taistelu(pelaaja, vihollinen):

    while pelaaja.hp > 0 or vihollinen.hp > 0:
        pelaajan_vuoro = True
        vihollisen_vuoro = True
        pelaaja_hp = 'HP: ' + str(pelaaja.hp) + '/' + str(pelaaja.maxhp)
        pelaaja_tp = 'TP: ' + str(pelaaja.taitopiste) + '/' + str(pelaaja.max_taitopiste)
        vihollinen_hp = 'HP: ' + str(vihollinen.hp) + '/' + str(vihollinen.maxhp)
        # Tulostaa pää-taistelu valikon
        print(f"  {'_'*100}\n"
              f" |{Fore.LIGHTYELLOW_EX}{'TAISTELE!':^49}{Style.RESET_ALL}|{Fore.LIGHTYELLOW_EX}{'TAISTELU LOKI':^50}{Style.RESET_ALL}|\n",
              f"|{'_'*49}|{'_'*50}|\n",
              f"|{Fore.LIGHTGREEN_EX}{pelaaja.nimi:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(1) Hyökkää':^17}{Style.RESET_ALL}|{Fore.LIGHTGREEN_EX}{vihollinen.nimi:^15}{Style.RESET_ALL}|{'':50}|\n",
              f"|{Fore.LIGHTRED_EX}{pelaaja_hp:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(2) Taidot ':^17}{Style.RESET_ALL}|{Fore.LIGHTRED_EX}{vihollinen_hp:^15}{Style.RESET_ALL}|{'':50}|\n",
              f"|{Fore.LIGHTMAGENTA_EX}{pelaaja_tp:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(3) Esineet':^17}{Style.RESET_ALL}|{'':15}|{'':50}|\n"
              f" |{'':15}|{'':17}|{'':15}|{'':50}|\n"
              f" |{'_'*15}|{'_'*17}|{'_'*15}|{'_'*50}|\n")
        # Tulostaa taidot valikon
        print(f"  {'_'*100}\n"
              f" |{Fore.LIGHTYELLOW_EX}{'TAIDOT!':^49}{Style.RESET_ALL}|{Fore.LIGHTYELLOW_EX}{'TAISTELU LOKI':^50}{Style.RESET_ALL}|\n",
              f"|{'_'*49}|{'_'*50}|\n",
              f"|{Fore.LIGHTGREEN_EX}{pelaaja.nimi:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(1) taito':^17}{Style.RESET_ALL}|{Fore.LIGHTGREEN_EX}{vihollinen.nimi:^15}{Style.RESET_ALL}|{'':50}|\n",
              f"|{Fore.LIGHTRED_EX}{pelaaja_hp:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(2) taito':^17}{Style.RESET_ALL}|{Fore.LIGHTRED_EX}{vihollinen_hp:^15}{Style.RESET_ALL}|{'':50}|\n",
              f"|{Fore.LIGHTMAGENTA_EX}{pelaaja_tp:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(3) taito':^17}{Style.RESET_ALL}|{'':15}|{'':50}|\n"
              f" |{'':15}|{Fore.LIGHTYELLOW_EX}{'(4) Takaisin':^17}{Style.RESET_ALL}|{'':15}|{'':50}|\n"
              f" |{'_' * 15}|{'_' * 17}|{'_' * 15}|{'_'*50}|\n")
        # Tulostaa esine valikon
        print(f"  {'_'*100}\n"
              f" |{Fore.LIGHTYELLOW_EX}{'ESINEET!':^49}{Style.RESET_ALL}|{Fore.LIGHTYELLOW_EX}{'TAISTELU LOKI':^50}{Style.RESET_ALL}|\n",
              f"|{'_'*49}|{'_'*50}|\n",
              f"|{Fore.LIGHTGREEN_EX}{pelaaja.nimi:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(1) Esine':^17}{Style.RESET_ALL}|{Fore.GREEN}{vihollinen.nimi:^15}{Style.RESET_ALL}|{'':50}|\n",
              f"|{Fore.LIGHTRED_EX}{pelaaja_hp:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(2) Esine':^17}{Style.RESET_ALL}|{Fore.RED}{vihollinen_hp:^15}{Style.RESET_ALL}|{'':50}|\n",
              f"|{Fore.LIGHTMAGENTA_EX}{pelaaja_tp:^15}{Style.RESET_ALL}|{Fore.LIGHTCYAN_EX}{'(3) Esine':^17}{Style.RESET_ALL}|{'':15}|{'':50}|\n"
              f" |{'':15}|{Fore.LIGHTYELLOW_EX}{'(4) Takaisin':^17}{Style.RESET_ALL}|{'':15}|{'':50}|\n"
              f" |{'_' * 15}|{'_' * 17}|{'_' * 15}|{'_'*50}|\n")
        input()


# Laskee taistelun mahdollisuuden
def taistelu_mahdollisuus_laskuri(matkan_paivat):

    heitto = random.randint(1, 20)

    if heitto + matkan_paivat > 12:
        print('Matkustit liian varomattomasti. Jouduit taisteluun!')
        input('\033[31mPaina Enter jatkaaksesi...\033[0m')
        return True

    elif heitto + matkan_paivat <= 12:
        print('Saavuit kohteeseen ilman taistelua')
        input('\033[31mPaina Enter jatkaaksesi...\033[0m')
        return False


# Tallentaa pelaajan tiedot peli tauluun
def tallennus(pelaaja):

    sql = f'''UPDATE peli SET pelaaja_sijainti = {pelaaja.sijainti},
              menneet_paivat = {pelaaja.menneet_paivat}, pelaaja_hp = {pelaaja.hp},
              pelaaja_taitopiste = {pelaaja.taitopiste} WHERE peli_id = {pelaaja.id}'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    print('Peli tallennettu')
    return


# Tulostaa taustatarinan jos käyttäjä syöttää halutun kirjaimen
def taustatarina():

    yn = input('Haluatko lukea taustatarinan ja ohjeet? Y/N: ')

    if yn.upper() == 'Y':
        print('kauan sitten diipadaapa')
        print(f'Seikkailusi alkaa kohteesta {nykyinen_sijainti["fantasia_nimi"]}')
        print('Tehtäväsi on löytää pahuksen sormus ja viedä se tulivuoreen')
        print('Voit matkustaa kohteisiin valitsemalla niitä edeltävän numeron')
        print('Yritä löytää sormus mahdollisimman nopeasti ja viedä se tulivuoreen,',
              'mutta pidemmälle matkustaessa riskit kasvavat')

    elif yn.upper() == 'N':
        print(f'Seikkailusi alkaa kohteesta {nykyinen_sijainti["fantasia_nimi"]}')

    input('\033[31mPaina Enter jatkaaksesi...\033[0m')


# Tarkastaa onko pelaajan sijainnissa sormus ja paluttaa arvon True tai False
def onko_kohteessa_sormus():

    if pelaaja.sijainti == sormus_sijainti:
        print('Löysit sormuksen!!')
        input('\033[31mPaina Enter jatkaaksesi...\033[0m')
        return True

    else:
        print('Kohteessa ei ole sormusta :(')
        input('\033[31mPaina Enter jatkaaksesi...\033[0m')
        return False


# PÄÄOHJELMA:

# Pelin alustus
winsound.PlaySound('adventure.wav', winsound.SND_LOOP | winsound.SND_ASYNC | winsound.SND_FILENAME)
pelaaja = paavalikko()
sormus_sijainti = sormus_arpominen()
nykyinen_sijainti = pelaajan_sijainti(pelaaja.id)


# Peli käynnissä
taustatarina()
while True:
# pelaaja valitsee minne haluaa matkustaa

    valinta = sijainti_valitsin(pelaaja)

# arvotaan taistelu etäisyyden perusteella

    if taistelu_mahdollisuus_laskuri(paivien_lisaaja(valinta, pelaaja)):
        taistelu(pelaaja, hae_random_vihollinen())

    paivien_lisaaja(valinta, pelaaja)

# tallennus taistelun jälkeen

    #tallennus(pelaaja) ei tallennusta testi vaiheessa
    nykyinen_sijainti = pelaajan_sijainti(pelaaja.id)

# Peli loppuu