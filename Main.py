import colorama
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

# TEKSTIVÄRIT:
punainen = colorama.Fore.LIGHTRED_EX
keltainen = colorama.Fore.LIGHTYELLOW_EX
syaani = colorama.Fore.LIGHTCYAN_EX
magenta = colorama.Fore.LIGHTMAGENTA_EX
vihrea = colorama.Fore.LIGHTGREEN_EX
sininen = colorama.Fore.LIGHTBLUE_EX
vari_reset = Style.RESET_ALL

# TIETOKANNAN ASETUKSET:

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
    def __init__(self, peli_id, pelaaja_nimi, pelaaja_sijainti, menneet_paivat, pelaaja_hp, pelaaja_maxhp,
                 pelaaja_suojaus, pelaaja_isku, pelaaja_taitopiste, pelaaja_max_taitopiste, onko_sormus, sormus_sijainti):
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
        self.sormus_sijainti = sormus_sijainti


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


# Lisää uuden rivin peli-tauluun eli luo uuden tallennuksen ja palauttaa tämän hetkisen tallennuksen id-arvon.
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


# Arpoo sormuksen sijainnin peli-tauluun
def sormus_arpominen(pelaaja):

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


# Tulostaa taisteluvalikon ja ohjaa taistelua
def taistelu(pelaaja, vihollinen):
    loki_txt1 = ''
    loki_txt2 = ''
    loki_txt3 = ''

    while True:
        pelaaja_hp = 'HP: ' + str(pelaaja.hp) + '/' + str(pelaaja.maxhp)
        pelaaja_tp = 'TP: ' + str(pelaaja.taitopiste) + '/' + str(pelaaja.max_taitopiste)
        vihollinen_hp = 'HP: ' + str(vihollinen.hp) + '/' + str(vihollinen.maxhp)

        # Tulostaa pää-taisteluvalikon
        print(f"  {'_'*100}\n"
              f" |{keltainen}{'TAISTELE!':^49}{vari_reset}|{keltainen}{'TAISTELU LOKI':^50}{vari_reset}|\n",
              f"|{'_'*49}|{'_'*50}|\n",
              f"|{vihrea}{pelaaja.nimi:^15}{vari_reset}|{syaani}{'(1) Hyökkää':^17}{vari_reset}|{vihrea}{vihollinen.nimi:^15}{vari_reset}|{keltainen}{loki_txt1:50}{vari_reset}|\n",
              f"|{punainen}{pelaaja_hp:^15}{vari_reset}|{syaani}{'(2) Taidot ':^17}{vari_reset}|{punainen}{vihollinen_hp:^15}{vari_reset}|{keltainen}{loki_txt2:50}{vari_reset}|\n",
              f"|{magenta}{pelaaja_tp:^15}{vari_reset}|{syaani}{'(3) Esineet':^17}{vari_reset}|{'':15}|{'':50}|\n"
              f" |{'':15}|{'':17}|{'':15}|{'':50}|\n"
              f" |{'_'*15}|{'_'*17}|{'_'*15}|{'_'*50}|\n")

        if pelaaja.hp <= 0:
            break

        if vihollinen.hp <= 0:
            break

        taistelu_paa_valinta = input(f"{keltainen}Valitse (1-3):{vari_reset}")

        if taistelu_paa_valinta == '1':
                loki_txt1 = perus_isku(pelaaja, vihollinen)
                loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)

        elif taistelu_paa_valinta == '2':
            vaara_taito_valinta_txt = ''

            while True:

                # Tulostaa taidot valikon
                print(f"  {'_'*100}\n"
                      f" |{keltainen}{'TAIDOT!':^49}{vari_reset}|{keltainen}{'TAISTELU LOKI':^50}{vari_reset}|\n",
                      f"|{'_'*49}|{'_'*50}|\n",
                      f"|{vihrea}{pelaaja.nimi:^15}{vari_reset}|{syaani}{'(1) taito':^17}{vari_reset}|{vihrea}{vihollinen.nimi:^15}{vari_reset}|{loki_txt1:50}|\n",
                      f"|{punainen}{pelaaja_hp:^15}{vari_reset}|{syaani}{'(2) taito':^17}{vari_reset}|{punainen}{vihollinen_hp:^15}{vari_reset}|{loki_txt2:50}|\n",
                      f"|{magenta}{pelaaja_tp:^15}{vari_reset}|{syaani}{'(3) taito':^17}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'':15}|{keltainen}{'(4) Takaisin':^17}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'_' * 15}|{'_' * 17}|{'_' * 15}|{'_'*50}|\n")
                print(f'{punainen}{vaara_taito_valinta_txt}{vari_reset}')
                taidot_valinta = input(f"{keltainen}Valitse (1-4):{vari_reset}")

                if taidot_valinta == '1':
                    break

                elif taidot_valinta == '2':
                    break

                elif taidot_valinta == '3':
                    break

                elif taidot_valinta == '4':
                    break

                else:
                    vaara_taito_valinta_txt = 'Väärä valinta!'

        elif taistelu_paa_valinta == '3':

            while True:

                # Tulostaa esinevalikon
                print(f"  {'_'*100}\n"
                      f" |{keltainen}{'ESINEET!':^49}{vari_reset}|{keltainen}{'TAISTELU LOKI':^50}{vari_reset}|\n",
                      f"|{'_'*49}|{'_'*50}|\n",
                      f"|{vihrea}{pelaaja.nimi:^15}{vari_reset}|{syaani}{'(1) Esine':^17}{vari_reset}|{vihrea}{vihollinen.nimi:^15}{vari_reset}|{keltainen}{loki_txt1:50}{vari_reset}|\n",
                      f"|{punainen}{pelaaja_hp:^15}{vari_reset}|{syaani}{'(2) Esine':^17}{vari_reset}|{punainen}{vihollinen_hp:^15}{vari_reset}|{keltainen}{loki_txt2:50}{vari_reset}|\n",
                      f"|{magenta}{pelaaja_tp:^15}{vari_reset}|{syaani}{'(3) Esine':^17}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'':15}|{keltainen}{'(4) Takaisin':^17}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'_' * 15}|{'_' * 17}|{'_' * 15}|{'_'*50}|\n")

                esine_valinta = input(f"{keltainen}Valitse (1-4):{vari_reset}")

                if esine_valinta == '1':
                    break

                elif esine_valinta == '2':
                    break

                elif esine_valinta == '3':
                    break

                elif esine_valinta == '4':
                    break

    if vihollinen.hp <= 0:
        input(f'{vihrea}Voitit Taistelun!{vari_reset}{keltainen} Paina Enter jatkaaksesi...{vari_reset}')

    if pelaaja.hp <= 0:
        input(f'{punainen}Voi ei! Hävisit taistelun!{vari_reset} {keltainen}Paina Enter jatkaaksesi...{vari_reset}')


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


# Tallentaa pelaajan tiedot peli-tauluun
def tallennus(pelaaja):

    sql = f'''UPDATE peli SET pelaaja_sijainti = {pelaaja.sijainti},
              menneet_paivat = {pelaaja.menneet_paivat}, pelaaja_hp = {pelaaja.hp},
              pelaaja_taitopiste = {pelaaja.taitopiste} WHERE peli_id = {pelaaja.id}'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    print('Peli tallennettu')
    return


def taitopisteen_kaytto(pelaaja):

    if pelaaja.taitopiste > 0:
        pelaaja.taitopiste -= 1

    else:
        print("Ei taitopisteitä jäljellä")


# Tulostaa taustatarinan, jos käyttäjä syöttää halutun kirjaimen
def taustatarina():

    yn = input('Haluatko lukea taustatarinan ja ohjeet? Y/N: ')

    if yn.upper() == 'Y':
        print(f'Pahuus on alkanut saastuttaa maailmaa. Tarujen mukaan kauan sitten kuollut {punainen}Dracula Vlad{vari_reset} on palannut.\n'
              'Hänet voi pysäyttää vain legendaarisen pahuksen sormuksen voimalla.')
        print(f'Tehtäväsi on löytää pahuksen sormus ja viedä se tulivuoreen jossa kohtaat {punainen}Dracula Vladin{vari_reset}.')
        print('Voit matkustaa kohteisiin valitsemalla niitä edeltävän numeron.')
        print('Yritä löytää sormus mahdollisimman nopeasti ja viedä se tulivuoreen,\n'
              'mutta muista, että mitä pidemmälle matkustat, sitä suurempi riski on kohdata Dracula Vladin kätyreitä.')
        print(f'Seikkailusi alkaa kohteesta {vihrea}{nykyinen_sijainti["fantasia_nimi"]}{vari_reset}.')
        print('')

    elif yn.upper() == 'N':
        print(f'Seikkailusi alkaa kohteesta {vihrea}{nykyinen_sijainti["fantasia_nimi"]}{vari_reset}')
        print('')
        input(f'{punainen}Paina Enter jatkaaksesi...{vari_reset}')



# Arpoo tuleeko event ja hakee sen randomilla taulusta
def tuleeko_event():

    if random.choice([True, False]) == True:
        sql = 'SELECT event.id FROM event ORDER BY RAND() LIMIT 1;'
        kursori = yhteys.cursor
        kursori.execute(sql)
        event = kursori.fetchone()

        return event


# Tarkastaa onko pelaajan sijainnissa sormus ja paluttaa arvon True tai False
def onko_kohteessa_sormus():

    if pelaaja.sijainti == sormus_sijainti:
        print('Löysit sormuksen!!')
        input('\033[31mPaina Enter jatkaaksesi...\033[0m')
        return True

    else:
        print(f'{punainen}Kohteessa ei ole sormusta{vari_reset}')
        print('')
        input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}')
        return False


# PÄÄOHJELMA:

# Pelin alustus
# winsound.PlaySound('adventure.wav', winsound.SND_LOOP | winsound.SND_ASYNC | winsound.SND_FILENAME)
pelaaja = paavalikko()
sormus_sijainti = sormus_arpominen()
nykyinen_sijainti = pelaajan_sijainti(pelaaja.id)


# Peli käynnissä
taustatarina()

while True:

    # pelaaja valitsee minne haluaa matkustaa
    valinta = int(sijainti_valitsin(pelaaja))

    # arvotaan taistelu etäisyyden perusteella
    if taistelu_mahdollisuus_laskuri(paivien_lisaaja(valinta, pelaaja)):
        taistelu(pelaaja, hae_random_vihollinen())

    paivien_lisaaja(valinta, pelaaja)

# tallennus taistelun jälkeen

    #tallennus(pelaaja) ei tallennusta testi vaiheessa
    nykyinen_sijainti = pelaajan_sijainti(pelaaja.id)

# Peli loppuu'
