import colorama
from colorama import Fore
from colorama import Style
import geopy
from geopy import distance
import mysql.connector
from mysql.connector import errorcode
import random
import sys
import time
import pygame
from PIL import Image
from eventit import event_valitsin


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
                 pelaaja_suojaus, pelaaja_isku, pelaaja_taitopiste, pelaaja_max_taitopiste,
                 onko_sormus, sormus_sijainti):
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

def alkusanat():

    print(f'\n\n\n{vihrea}{"Tämä peli on luotu käyttäen hiilineutraalia sähköä."}{vari_reset} \n\n'
          f'Suosittelemme käyttämään tummaa taustaa pelatessa.\n\n'
          f'Pelissä sinulle annetaan vaihtoehtoja, jotka valitaan tietyllä numeronäppäimillä tai kirjaimilla {keltainen}Y{vari_reset} tai {keltainen}N{vari_reset}. \n'
          f'Aina kun on kirjoitettu haluttu toiminta, painetaan {keltainen}Enter{vari_reset} suorittaakseen se. \n\n')

    input(f'{keltainen}Paina Enter jatkaaksesi päävalikkoon{vari_reset}')
    print(f'\n\n\n\n')


def  esineiden_haku(pelaaja):

    sql = (f'SELECT esine_nimi, esineen_id FROM inventaario, esineet, peli WHERE esineen_id = esine_id AND pelaajan_id = "{str(pelaaja.id)}" AND peli_id = "{str(pelaaja.id)}"')
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    inventaario_lista = kursori.fetchall()


    return inventaario_lista


def esineen_arvonta(inventaario):

    randomi = random.randint(1, 20)

    if randomi >= 10:

        sql = 'SELECT esine_nimi, esine_id AS esineen_id FROM esineet ORDER by RAND() LIMIT 1'
        kursori = yhteys.cursor(dictionary=True)
        kursori.execute(sql)
        random_esine = kursori.fetchone()
        print('')
        print(f"Sait esineen: {vihrea}{random_esine['esine_nimi']}{vari_reset}")
        print('')
        inventaario.append(random_esine)

    else:
        print('')
        print(f'Et löytänyt esineitä')
        print('')

    return


def haluatko_nukkua(pelaaja):

    pelaaja_hp = 'HP: ' + str(pelaaja.hp) + '/' + str(pelaaja.maxhp)
    pelaaja_tp = 'TP: ' + str(pelaaja.taitopiste) + '/' + str(pelaaja.max_taitopiste)
    viiva = '_'
    while True:

        print(f"{viiva * 17}\n"
              f"|{vihrea}{pelaaja.nimi:^15}{vari_reset}|\n"
              f"|{punainen}{pelaaja_hp:^15}{vari_reset}|\n"
              f"|{magenta}{pelaaja_tp:^15}{vari_reset}|\n"
              f"|{viiva * 15}|\n\n")

        valinta = input(f'Haluatko levätä yhden päivän ja palauttaa {punainen}HP{vari_reset} ja {magenta}TP{vari_reset} täysille? {keltainen}Y/N{vari_reset}\n')

        while valinta.upper() != 'Y' and valinta.upper() != 'N':

            valinta = input('Virheellinen syöte. kirjoita Y (kyllä) tai N (ei) ')

        else:
            break

    if valinta.upper() == 'Y':
        pelaaja.hp = pelaaja.maxhp
        pelaaja.taitopiste = pelaaja.max_taitopiste
        pelaaja.menneet_paivat += 1
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/efektit/mies_kuorsaa.wav'), 0, 4000)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/musiikki/nukkuu.wav'), 0, 4000)
        time.sleep(4)
        vaihtaa_aanet(pelaaja)

    else:
        print('Päätit jatkaa lepäämättä. Rohkeaa.')


# Hakee kaikki kohteet paitsi pelaajan kohteen
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

    sql = 'SELECT * FROM viholliset WHERE bossi = "0" ORDER by RAND() LIMIT 1'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    haku_tiedot = kursori.fetchone()
    vihollinen = Vihollinen(haku_tiedot['vihollinen_id'], haku_tiedot['vihollinen_nimi'], haku_tiedot['vihollinen_hp'],
                            haku_tiedot['vihollinen_maksimi_hp'], haku_tiedot['vihollinen_suojaus'],
                            haku_tiedot['vihollinen_isku'])
    return vihollinen


def hae_bossi():

    sql = 'SELECT * FROM viholliset WHERE bossi = "1" ORDER by RAND() LIMIT 1'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    haku_tiedot = kursori.fetchone()
    vihollinen = Vihollinen(haku_tiedot['vihollinen_id'], haku_tiedot['vihollinen_nimi'], haku_tiedot['vihollinen_hp'],
                            haku_tiedot['vihollinen_maksimi_hp'], haku_tiedot['vihollinen_suojaus'],
                            haku_tiedot['vihollinen_isku'])
    return vihollinen


def km_to_day(matka):

    if matka < 75:
        aika = 1
        return aika

    elif matka < 125:
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

    sql = f'SELECT pelaaja_nimi FROM peli;'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    pelaajat = kursori.fetchall()

    while True:
        nimi = input('Anna hahmollesi nimi: ')

        varattu = False

        for kayttaja in pelaajat:

            if nimi.upper() == str(kayttaja["pelaaja_nimi"]).upper():
                varattu = True

        if varattu == True:

            print('Käyttäjänimi on varattu')

        elif len(nimi) < 2:

            print('Nimen minimipituus on 2 merkkiä.')

        elif len(nimi) > 12:

            print('Nimen maksimipituus on 12 merkkiä pitkä.')

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
                      haku_tiedot['pelaaja_taitopiste'], haku_tiedot['pelaaja_maksimi_taitopiste'],
                      haku_tiedot['onko_sormus'], haku_tiedot['sormus_sijainti'])
    return pelaaja


# Tulostaa käyttäjälle tallennukset ja palauttaa käyttäjän syötteen
def lataa_peli(tallennetut_pelit):

    for tallennus in tallennetut_pelit:
        print(f"{keltainen}{tallennus['peli_id']}{vari_reset}. {vihrea}{tallennus['pelaaja_nimi']}{vari_reset}")

    print('')
    while True:
        valinta = input(f'Mitä tallennusta haluat jatkaa? Kirjoita {keltainen}numero{vari_reset} ja paina {keltainen}Enter{vari_reset}\n')
        tallennus_haku = False

        for tallennus in tallennetut_pelit:

            if valinta == str(tallennus['peli_id']):
                tallennus_haku = True
                print(f'{keltainen}{valinta}{vari_reset} valittu.\n\n')
                break

        if tallennus_haku == True:
            break

        print(f"{punainen}Ei löydy tallennusta valinnalla!{vari_reset}\n")

    return valinta


# Tarkastaa onko pelaajan sijainnissa sormus ja paluttaa arvon True tai False
def onko_kohteessa_sormus(pelaaja):

    if pelaaja.onko_sormus == 0:

        if int(pelaaja.sijainti) == int(pelaaja.sormus_sijainti):
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('aanet/efektit/sormusloytynyt.mp3'))
            print(f'{vihrea}Löysit sormuksen!!{vari_reset}\n\n')
            pelaaja.onko_sormus = 1
            input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}')
            return True

        else:
            print(f'{punainen}Kohteessa ei ole sormusta{vari_reset}\n')
            input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
            return False


def paavalikko():

    # Ottaa vastaan käyttäjän näppäinpainalluksen ja toteuttaa sen perusteella tietyn funktion
    while True:

        sql = 'SELECT peli_id, pelaaja_nimi FROM peli '
        kursori = yhteys.cursor(dictionary=True)
        kursori.execute(sql)
        tallennetut_pelit = kursori.fetchall()

        # Hakee paavalikkoTeksti.txt tiedoston ja tulostaa visuaalisen tekstin
        for x in open(file="tekstitiedostot/paavalikkoTeksti.txt"):
            print(f"        {magenta}{x}{vari_reset}", end="")

        # Hakee uusi_peli.txt tiedoston ja tulostaa  visuaalisen tekstin
        for x in open(file="tekstitiedostot/uusi_peli.txt"):
            print(f"        {vihrea}{x}{vari_reset}", end="")

        # Hakee txt tiedoston ja tulostaa päävalikon visuaalisen tekstin
        for x in open(file="tekstitiedostot/lataa_peli.txt"):
            print(f"        {keltainen}{x}{vari_reset}", end="")

        # Hakee txt tiedoston ja tulostaa päävalikon visuaalisen tekstin
        for x in open(file="tekstitiedostot/pisteet.txt"
                           ""):
            print(f"        {syaani}{x}{vari_reset}", end="")

        # Hakee txt tiedoston ja tulostaa päävalikon visuaalisen tekstin
        for x in open(file="tekstitiedostot/poistu.txt"):
            print(f"        {punainen}{x}{vari_reset}", end="")

        valinta = input()

        if valinta == "1":

            pelaaja = luo_pelaaja(luo_peli())
            pelaaja.sormus_sijainti = sormus_arpominen(pelaaja)
            vaihtaa_aanet(pelaaja)
            break

        if valinta == "2":

            if len(tallennetut_pelit) == 0:
                print(f"{punainen}Tallennuksia ei löytynyt!{vari_reset}")
                input(f"{keltainen}Paina Enter jatkaaksesi takaisin päävalikkoon...{vari_reset}")
                continue

            pelaaja = luo_pelaaja(lataa_peli(tallennetut_pelit))
            vaihtaa_aanet(pelaaja)
            break

        if valinta == "3":
            pisteet()
            continue

        if valinta == "4":
            poistu()

    return pelaaja


def paivien_lisaaja(haluttu_kohde_id, pelaaja):

    sql = f'''SELECT airport.id, airport.fantasia_nimi, airport.latitude_deg, airport.longitude_deg 
              FROM airport WHERE airport.id = "{haluttu_kohde_id}"'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    kohde = kursori.fetchone()
    loppu_koordinaatit = kohde['latitude_deg'], kohde['longitude_deg']
    alku_koordinaatit = nykyinen_sijainti['latitude_deg'], nykyinen_sijainti['longitude_deg']
    matka = distance.distance(alku_koordinaatit, loppu_koordinaatit).km

    return km_to_day(matka)


#hakee pisteet
def pisteet():
    sql = f'''SELECT nimi, paivat FROM pisteet ORDER BY (paivat) LIMIT 10;'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    top = kursori.fetchall()

    print(f'{keltainen}{"TOP 10":^34}{vari_reset}\n')
    i = 1
    for sankari in top:
        print(f'{i:2} {vihrea}{sankari["nimi"]:14}{vari_reset}{syaani}{sankari["paivat"]:<8}{vari_reset}{keltainen}päivää{vari_reset}')
        i = i + 1
    print('')
    input(f'{keltainen}Paina Enter palataksesi valikkoon...{vari_reset}\n')



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


def pelaajan_sijainti_tiedot_haku(pelaaja):

    sql = f'''SELECT airport.id, airport.fantasia_nimi, airport.latitude_deg, airport.longitude_deg
              FROM airport
              WHERE airport.id = "{pelaaja.sijainti}"'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    tiedot = kursori.fetchone()
    #print(tiedot)
    return tiedot


def perus_isku(pelaaja, vihollinen):

    if pelaaja.hp > 0:

        isku_osuma = random.randint(1, 20) + 2

        if isku_osuma >= vihollinen.suojaus:
            isku = random.randint(1, pelaaja.isku) + 2
            vihollinen.hp = int(vihollinen.hp) - isku
            loki_printtaus1 = f'Teit {isku} vahinkoa!'
            random_aani= random.randint(1,3)

            if random_aani == 1:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/isku_perus2.wav'))

            elif random_aani == 2:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/isku_perus3.wav'))

            elif random_aani == 3:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/isku_perus1.wav'))

        else:
            loki_printtaus1 = 'Vihollinen väisti iskusi.'
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/huti.wav'))

    else:
        loki_printtaus1 = 'Olet kuollut.'

    return loki_printtaus1


# Viholisen perusisku
def perus_isku_vihollinen(vihollinen, pelaaja):

    if vihollinen.hp > 0:

        isku_osuma = random.randint(1, 20) + 2

        if isku_osuma >= pelaaja.suojaus:

            isku = random.randint(1, vihollinen.isku) + 2
            pelaaja.hp -= isku

            if pelaaja.hp < 0:
                pelaaja.hp = 0

            loki_printtaus2 = f'Vihollinen teki {isku} vahinkoa!'
            time.sleep(0.2)
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('aanet/efektit/mies_sattuu.wav'))

        else:
            loki_printtaus2 = f'Väistit vihollisen iskun!'
            time.sleep(0.2)
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('aanet/efektit/huti.wav'))

    else:
        loki_printtaus2 = f'Vihollinen kuoli!'

    return loki_printtaus2


# Tulostaa pelaajalle kohteet ja etäisyydet. Palauttaa valitun kohteen id:n
def sijainti_valitsin(pelaaja):

    id_lista = []
    oikea_kohde = 0

    for kohde in hae_kaikki_kohteet(pelaaja):
        loppu_koordinaatit = kohde['latitude_deg'], kohde['longitude_deg']
        alku_koordinaatit = nykyinen_sijainti['latitude_deg'], nykyinen_sijainti['longitude_deg']
        matka = distance.distance(alku_koordinaatit, loppu_koordinaatit).km

        if matka < 75:
            print(f"{keltainen}{kohde['id']:2}{vari_reset}. Kohteeseen {syaani}{kohde['fantasia_nimi']:28}{vari_reset} {punainen}{km_to_day(matka)}{vari_reset} päivän matkustus.")
            id_lista.append(kohde['id'])

        elif matka < 125:
            print(f"{keltainen}{kohde['id']:2}{vari_reset}. Kohteeseen {syaani}{kohde['fantasia_nimi']:28}{vari_reset} {punainen}{km_to_day(matka)}{vari_reset} päivän matkustus.")
            id_lista.append(kohde['id'])

        elif matka < 200:
            print(f"{keltainen}{kohde['id']:2}{vari_reset}. Kohteeseen {syaani}{kohde['fantasia_nimi']:28}{vari_reset} {punainen}{km_to_day(matka)}{vari_reset} päivän matkustus.")
            id_lista.append(kohde['id'])

        elif matka > 200:
            print(f"{keltainen}{kohde['id']:2}{vari_reset}. Kohteeseen {syaani}{kohde['fantasia_nimi']:28}{vari_reset} {punainen}{km_to_day(matka)}{vari_reset} päivän matkustus.")
            id_lista.append(kohde['id'])

    print(f'\nOlet kohteessa {vihrea}{nykyinen_sijainti["fantasia_nimi"]}{vari_reset}\n\n'
          f"Seikkailuun on kulunut: {keltainen}{pelaaja.menneet_paivat}{vari_reset} päivää\n")


    while True:

        valinta = input(f'Mihin kohteeseen haluat matkustaa? Kirjoita {keltainen}numero{vari_reset} ja paina {keltainen}Enter{vari_reset}\n'
                        f'Tai jos haluat avata kartan ensin kirjoita {keltainen}{"M"}{vari_reset} ja paina {keltainen}Enter{vari_reset}\n')

        if valinta.upper() == 'M':
            kartta = Image.open("kuvat/kartta.png")
            kartta.show()
            continue

        for id in id_lista:

            if str(id) == valinta:
                print(f'{keltainen}{valinta} valittu!{vari_reset}')
                oikea_kohde = 1

        if oikea_kohde == 1:
            break

        else:
            print(f'{punainen}Virheellinen kohde.{vari_reset}')

    pygame.mixer.Channel(1).play(pygame.mixer.Sound(
        'aanet/efektit/askeleet_hiekka.wav'), 0, 2400)
    return valinta


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
    return sijainti_id['id']

# Hakee taidot
def taito_haku(pelaaja):

    sql = f'SELECT taito_nimi FROM taidot'
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)
    taito_lista = kursori.fetchall()

    return taito_lista


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
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/mies_kuolee.wav'))
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

                try:
                    taito1 = taidot[0]['taito_nimi']
                except:
                    taito1 = 'Tyhjä'

                try:
                    taito2 = 'Tyhjä'
                except:
                    taito2 = 'Tyhjä'

                try:
                    taito3 = 'Tyhjä'
                except:
                    taito3 = 'Tyhjä'

                # Tulostaa taidot valikon
                print(f"  {'_'*100}\n"
                      f" |{keltainen}{'TAIDOT!':^49}{vari_reset}|{keltainen}{'TAISTELU LOKI':^50}{vari_reset}|\n",
                      f"|{'_'*49}|{'_'*50}|\n",
                      f"|{vihrea}{pelaaja.nimi:^15}{vari_reset}|{keltainen}{' (1)':<4}{vari_reset}{syaani}{taito1:^13}{vari_reset}|{vihrea}{vihollinen.nimi:^15}{vari_reset}|{keltainen}{loki_txt1:50}{vari_reset}|\n",
                      f"|{punainen}{pelaaja_hp:^15}{vari_reset}|{keltainen}{' (2)':<4}{vari_reset}{syaani}{taito2:^13}{vari_reset}|{punainen}{vihollinen_hp:^15}{vari_reset}|{keltainen}{loki_txt2:50}{vari_reset}|\n",
                      f"|{magenta}{pelaaja_tp:^15}{vari_reset}|{keltainen}{' (3)':<4}{vari_reset}{syaani}{taito3:^13}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'':15}|{keltainen}{' (4)':<4}{'Takaisin':^13}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'_' * 15}|{'_' * 17}|{'_' * 15}|{'_'*50}|\n")
                print(f'{punainen}{vaara_taito_valinta_txt}{vari_reset}')
                taidot_valinta = input(f"{keltainen}Valitse (1-4):{vari_reset}")

                if taidot_valinta == '1':

                    if taito1 == 'tulipallo' and pelaaja.taitopiste > 0:
                        loki_txt1 = tulipallo(pelaaja, vihollinen)
                        loki_txt2 = perus_isku_vihollinen(vihollinen,pelaaja)
                        break

                    if taito1 == 'Tyhjä':
                        vaara_taito_valinta_txt = 'Taitoa ei ole paikassa 1'

                elif taidot_valinta == '2':

                    if taito2 == 'Tyhjä':
                        vaara_taito_valinta_txt = 'Taitoa ei ole paikassa 2'

                elif taidot_valinta == '3':

                    if taito3 == 'Tyhjä':
                        vaara_taito_valinta_txt = 'Taitoa ei ole paikassa 3'

                elif taidot_valinta == '4':
                    break

                else:
                    vaara_taito_valinta_txt = 'Väärä valinta!'

        elif taistelu_paa_valinta == '3':
            vaara_esine_valinta_txt = ''

            while True:

                try:
                    esine1 = inventaario[0]['esine_nimi']
                except:
                    esine1 = 'Tyhjä'

                try:
                    esine2 = inventaario[1]['esine_nimi']
                except:
                    esine2 = 'Tyhjä'

                try:
                    esine3 = inventaario[2]['esine_nimi']
                except:
                    esine3 = 'Tyhjä'

                # Tulostaa esinevalikon
                print(f"  {'_'*100}\n"
                      f" |{keltainen}{'ESINEET!':^49}{vari_reset}|{keltainen}{'TAISTELU LOKI':^50}{vari_reset}|\n",
                      f"|{'_'*49}|{'_'*50}|\n",
                      f"|{vihrea}{pelaaja.nimi:^15}{vari_reset}|{keltainen}{' (1)':<4}{vari_reset}{syaani}{esine1:^13}{vari_reset}|{vihrea}{vihollinen.nimi:^15}{vari_reset}|{keltainen}{loki_txt1:50}{vari_reset}|\n",
                      f"|{punainen}{pelaaja_hp:^15}{vari_reset}|{keltainen}{' (2)':<4}{vari_reset}{syaani}{esine2:^13}{vari_reset}|{punainen}{vihollinen_hp:^15}{vari_reset}|{keltainen}{loki_txt2:50}{vari_reset}|\n",
                      f"|{magenta}{pelaaja_tp:^15}{vari_reset}|{keltainen}{' (3)':<4}{vari_reset}{syaani}{esine3:^13}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'':15}|{keltainen}{' (4)':<4}{'Takaisin':^13}{vari_reset}|{'':15}|{'':50}|\n"
                      f" |{'_' * 15}|{'_' * 17}|{'_' * 15}|{'_'*50}|\n")

                print(f'{punainen}{vaara_esine_valinta_txt}{vari_reset}')
                esine_valinta = input(f"{keltainen}Valitse (1-4):{vari_reset}")

                if esine_valinta == '1':

                    if esine1 == 'eliksiiri':
                        loki_txt1 = eliksiiri(pelaaja)
                        inventaario.pop(0)
                        loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)
                        break

                    if esine1 == 'taitojuoma':
                        loki_txt1 = taitojuoma(pelaaja)
                        inventaario.pop(0)
                        loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)
                        break

                    if esine1 == 'Tyhjä':
                        vaara_esine_valinta_txt = 'Esinettä ei ole paikassa 1'

                elif esine_valinta == '2':

                    if esine2 == 'eliksiiri':
                        loki_txt1 = eliksiiri(pelaaja)
                        inventaario.pop(1)
                        loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)
                        break

                    if esine2 == 'taitojuoma':
                        loki_txt1 = taitojuoma(pelaaja)
                        inventaario.pop(0)
                        loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)
                        break

                    if esine2 == 'Tyhjä':
                        vaara_esine_valinta_txt ='Esinettä ei ole paikassa 2'

                elif esine_valinta == '3':

                    if esine3 == 'eliksiiri':
                        loki_txt1 = eliksiiri(pelaaja)
                        inventaario.pop(2)
                        loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)
                        break

                    if esine3 == 'taitojuoma':
                        loki_txt1 = taitojuoma(pelaaja)
                        inventaario.pop(0)
                        loki_txt2 = perus_isku_vihollinen(vihollinen, pelaaja)
                        break

                    if esine3 == 'Tyhjä':
                        vaara_esine_valinta_txt ='Esinettä ei ole paikassa 3'

                elif esine_valinta == '4':
                    break

                else:
                    vaara_esine_valinta_txt = 'Väärä valinta!'

    if vihollinen.hp <= 0:
        input(f'{vihrea}Voitit Taistelun!{vari_reset}{keltainen} Paina Enter jatkaaksesi...{vari_reset}\n')
        return True

    if pelaaja.hp <= 0:
        input(f'{punainen}Voi ei! Hävisit taistelun!{vari_reset} {keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
        return False


# Laskee taistelun mahdollisuuden
def taistelu_mahdollisuus_laskuri(matkan_paivat):

    heitto = random.randint(1, 20)

    if heitto + matkan_paivat > 10:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/taistelu_alkaa.mp3'))
        print(f'{punainen}Matkustit liian varomattomasti. Jouduit taisteluun!{vari_reset}\n')
        input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
        vaitaa_aanet_taistelu()
        return True

    elif heitto + matkan_paivat <= 10:
        print(f'{vihrea}Saavuit kohteeseen ilman taistelua{vari_reset}\n')
        input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
        return False


# Tallentaa pelaajan tiedot peli-tauluun
def tallennus(pelaaja, inventaario):

    sql = f'''UPDATE peli SET pelaaja_sijainti = {pelaaja.sijainti},
              menneet_paivat = {pelaaja.menneet_paivat}, pelaaja_hp = {pelaaja.hp},
              pelaaja_taitopiste = {pelaaja.taitopiste}, onko_sormus = {pelaaja.onko_sormus} 
              WHERE peli_id = {pelaaja.id}'''
    kursori = yhteys.cursor(dictionary=True)
    kursori.execute(sql)

    sql = f'DELETE FROM inventaario WHERE pelaajan_id = "{int(pelaaja.id)}"'
    kursori = yhteys.cursor()
    kursori.execute(sql)

    for esine in  inventaario:
        sql = f'INSERT INTO inventaario (pelaajan_id, esineen_id) VALUES ({pelaaja.id}, {esine["esineen_id"]})'
        kursori = yhteys.cursor(dictionary=True)
        kursori.execute(sql)

    print(f'{keltainen}\nPeli tallennettu\n{vari_reset}')
    return


def tallennuksen_poisto_ja_pisteet(pelaaja):

    sql = (f'''INSERT INTO pisteet (id, nimi, paivat) VALUES ("{int(pelaaja.id)}", "{str(pelaaja.nimi)}", "{int(pelaaja.menneet_paivat)}")''')
    kursori = yhteys.cursor()
    kursori.execute(sql)

    sql = (f'DELETE FROM inventaario WHERE pelaajan_id = "{int(pelaaja.id)}";')
    kursori.execute(sql)
    sql = (f'DELETE FROM peli WHERE peli_id = "{int(pelaaja.id)}";')
    kursori.execute(sql)
    print(f'{keltainen}Tallennuksesi on poistettu ja suorituksesti on lisätty piste tauluun.{vari_reset}')


def kuolema_pelin_poisto(pelaaja):

    sql = (f'DELETE FROM inventaario WHERE pelaajan_id = "{int(pelaaja.id)}";')
    kursori = yhteys.cursor()
    kursori.execute(sql)
    sql = (f'DELETE FROM peli WHERE peli_id = "{int(pelaaja.id)}";')
    kursori.execute(sql)


# Tulostaa taustatarinan, jos käyttäjä syöttää halutun kirjaimen
def taustatarina():

    while True:
        yn = input(f'Haluatko lukea taustatarinan ja ohjeet?{keltainen}Y/N: {vari_reset}\n')

        if yn.upper() == 'Y':
            for x in open(file="tekstitiedostot/alkutarina.txt",encoding="utf-8"):
                print(f"{keltainen}{str(x)}{vari_reset}", end="")
            input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
            break

        if yn.upper() == 'N':
            print(f'Seikkailusi alkaa kohteesta {vihrea}{nykyinen_sijainti["fantasia_nimi"]}{vari_reset}\n')
            input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
            break

        else:
            print(f'{punainen}Väärä valinta!{vari_reset}\n\n')


# Arpoo tuleeko event ja hakee sen randomilla taulusta
def tuleeko_event():

    if random.choice([True, False]) == True:

        sql = 'SELECT event.id FROM event ORDER BY RAND() LIMIT 1;'
        kursori = yhteys.cursor
        kursori.execute(sql)
        event = kursori.fetchone()
        return event


# Vaihtaa musiikin. Taistelua varten
def vaitaa_aanet_taistelu():

    aani = random.randint(1, 7)

    if aani == 1:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki1.mp3'), -1)
        pygame.mixer.Channel(1).pause()

    if aani == 2:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki2.mp3'), -1)
        pygame.mixer.Channel(1).pause()

    if aani == 3:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki3.mp3'), -1)
        pygame.mixer.Channel(1).pause()

    if aani == 4:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki4.mp3'), -1)
        pygame.mixer.Channel(1).pause()

    if aani == 5:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki5.mp3'), -1)
        pygame.mixer.Channel(1).pause()

    if aani == 6:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki6.mp3'), -1)
        pygame.mixer.Channel(1).pause()

    if aani == 7:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/taistelu_musiikki7.mp3'), -1)
        pygame.mixer.Channel(1).pause()


# Vaihtaa äänet pelaajan sijainnin perusteella
def vaihtaa_aanet(pelaaja):

    # Uudentoivon-kylä
    if pelaaja.sijainti == 1:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/uudentoivon-kyla_musiikki.wav'), -1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/uudentoivon-kyla_tausta.wav'), -1, )

    # Ruoholaakso
    if pelaaja.sijainti == 2:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/tausta/ruoholaakso_tausta.wav'), -1)
        pygame.mixer.Channel(1).pause()

    # Velhotorni
    if pelaaja.sijainti == 3:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/velhotorni_musiikki.wav'), -1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/velhotorni_tausta.wav'), -1, )

    # Varisräme
    if pelaaja.sijainti == 4:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/varisräme_tausta.wav'), -1, )

    # Noitametsä
    if pelaaja.sijainti == 5:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/noitametsä_tausta.wav'), -1, )

    # Sammakkojärvi
    if pelaaja.sijainti == 6:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/sammakkojärvi_tausta.wav'), -1)

    # Suurentarmon-kaupunki
    if pelaaja.sijainti == 7:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/suurentarmon-kaupunki_musiikki.wav'), -1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/suurentarmon-kaupunki_tausta.wav'), -1, )

    # Hiisisuo
    if pelaaja.sijainti == 8:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/hiisisuo_tausta.wav'), -1, )

    # Peikkoluola
    if pelaaja.sijainti == 9:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/peikkoluola_tausta.wav'), -1, )

    # Tulivuori
    if pelaaja.sijainti == 10:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/tausta/tulivuori_tausta.wav'), -1, )


# ESINEET:
def eliksiiri(pelaaja):

    parannus_arvo = (random.randint(1, 4) * 3) + 2
    parannettu_maara = 0

    for x in range(0, parannus_arvo):
        if pelaaja.hp == pelaaja.maxhp:
            break
        pelaaja.hp += 1
        parannettu_maara += 1

    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/eliksiiri1.wav'))
    time.sleep(0.2)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/eliksiiri2.wav'), 0, 910)
    time.sleep(0.9)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/nielee.wav'))
    time.sleep(0.3)
    palautettava_teksti = f'Eliksiiri paransi {parannettu_maara} elämä pistettä'
    return palautettava_teksti


def taitojuoma(pelaaja):

    parannus_arvo = 3
    parannettu_maara = 0

    for x in range(0, parannus_arvo):
        if pelaaja.taitopiste == pelaaja.max_taitopiste:
            break
        pelaaja.taitopiste += 1
        parannettu_maara += 1

    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/eliksiiri1.wav'))
    time.sleep(0.2)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/eliksiiri2.wav'), 0, 910)
    time.sleep(0.9)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/nielee.wav'))
    time.sleep(0.3)
    palautettava_teksti = f'Sait {parannettu_maara} taitopistettä'
    return palautettava_teksti


# TAIDOT:
def tulipallo(pelaaja, vihollinen):

    vahinko_arvo = (random.randint(1, 6) * 2) + 2
    pelaaja.taitopiste -= 1
    vihollinen.hp -= vahinko_arvo
    if vihollinen.hp < 0:
        vihollinen.hp = 0
    palautettava_teksti = f'Tulipallo käristi {vahinko_arvo} elämäpistettä viholliselta'
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('aanet/efektit/tulipallo.wav'))
    return palautettava_teksti


# PÄÄOHJELMA:

# Ääni asetukset
pygame.mixer.init()
pygame.mixer.Channel(0).set_volume(0.06)
pygame.mixer.Channel(1).set_volume(0.2)
pygame.mixer.Channel(2).set_volume(0.2)

# Pelin alustus
alkusanat()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/paavalikko_musiikki.wav'), -1)
pelaaja = paavalikko()
nykyinen_sijainti = pelaajan_sijainti(pelaaja.id)
inventaario = esineiden_haku(pelaaja)
taidot = taito_haku(pelaaja)
peli_lapi = False


# Peli käynnissä
taustatarina()

while peli_lapi == False:

    # Pelaaja valitsee minne haluaa matkustaa
    valinta = int(sijainti_valitsin(pelaaja))

    # Arvotaan tuleeko taistelu etäisyyden perusteella
    if taistelu_mahdollisuus_laskuri(paivien_lisaaja(valinta, pelaaja)) == True:

        # Taistelu!
        if taistelu(pelaaja, hae_random_vihollinen()) == True:

            # Tarkistetaan mahtuuko pelaajalle esineitä
            if len(inventaario) < 3:

                # Arvotaan random esine
                esineen_arvonta(inventaario)

            else:
                print(f'{punainen}Sinulle ei mahdu esineitä{vari_reset}')

            # Lisätään pelaaja olioon päivät
            pelaaja.menneet_paivat += paivien_lisaaja(valinta, pelaaja)

            # Päivitetään pelaaja olion sijainti taistelun jälkeen
            pelaaja.sijainti = int(valinta)

            # Vaihtaa äänet sijainnin perusteella
            vaihtaa_aanet(pelaaja)

        else:
            # Jos pelaaja kuolee taistelussa, poistetaan tallennus
            print(f'{punainen}Sinä kuolit. Tallennuksesi on poistettu{vari_reset}')
            kuolema_pelin_poisto(pelaaja)
            break

    else:
        # Jos pelaaja ei joudu taisteluun, lisätään päivät pelaaja olioon
        pelaaja.menneet_paivat += paivien_lisaaja(valinta, pelaaja)

        # Päivitetään pelaajan sijainti taistelun jälkeen
        pelaaja.sijainti = int(valinta)

        # Vaihtaa äänet sijainnin perusteella
        vaihtaa_aanet(pelaaja)

        # Hakee eventin kohteen perusteella
        event_valitsin(pelaaja)

        # Katsotaan kuoliko pelaaja
        if pelaaja.hp <= 0:
            print('Sinä kuolit. Tallennuksesi on poistettu')
            kuolema_pelin_poisto(pelaaja)
            break

    # Haetaan tiedot nykyisestä sijainnista pelaaja olion sijainnin perusteella
    nykyinen_sijainti = pelaajan_sijainti_tiedot_haku(pelaaja)

    # Tarkistaa onko kohteessa sormusta. Jos on se lisää sen pelaajalle
    onko_kohteessa_sormus(pelaaja)

    # Kysytään haluaako pelaaja nukkua, jos pelaaja on menettänyt HP tai TP
    if pelaaja.hp != pelaaja.maxhp or pelaaja.taitopiste != pelaaja.max_taitopiste:
        haluatko_nukkua(pelaaja)

    # Tarkistetaan onko pelaaja tulivuorella ja onko pelaajalla sormus
    if pelaaja.sijainti == 10 and pelaaja.onko_sormus == 1:

        print(f'Olet saapunut tulivuoren huipulle. Allasi hehkuu valtava laavameri.\n'
              f'Pitelet sormusta kädessäsi, valmiina heittämään sen tulivuoreen...\n'
              f'Yhtäkkiä sormus alkaa polttaa kädessäsi ja se putoaa jalkoihisi.\n'
              f'Näät kuinka sormus alkaa hehkua ja alkaa sen ympärille myodustumaan valtava musta savupilvi\n'
              f'Savupilvestä astuu ulos sormuksen kuolleen haltijan {punainen}Gorgonin{vari_reset} henki.\n')

        print(f'{punainen}Gorgon: "Maailma on MINUN! Valmistaudu KUOLEMAAN!"\n')
        input(f'{keltainen}Paina Enter aloittaaksesi viimeinen taistelu...{vari_reset}\n')

        # Bossfight äänet
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/gorgon_taistelu.wav'), -1)

        # Tarkistaa viimeisen taistelun tuloksen.
        if taistelu(pelaaja, hae_bossi()) == True:

            print(f'Olet päihittänyt sormuksen herran, sinulla on nyt edessäsi elämäsi tärkein valinta...\n')

            # Pelaaja valitsee kahdesta eri lopetuksesta
            while True:
                lopetus = input(f'Valitse: {keltainen}(1){vari_reset} {vihrea}Heitä sormus tulivuoreen.{vari_reset} tai {keltainen}(2){vari_reset} {punainen}Ota haltuun sormuksen voima.{vari_reset}\n')

                # Varmistetaan oikea valinta.# Ei hyväksytä virheellistä.
                if lopetus == '1' or lopetus == '2':
                    break

                # Ei hyväksytä virheellistä.
                else:
                    print(f'Tee valinta! {vihrea}(1){vari_reset} tai {punainen}(2){vari_reset}:\n')

            # Hyvä lopetus
            if lopetus == '1':
                # Tausta_musiikki vaihtuu
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/paavalikko_musiikki.wav'))

                print(f'Heität sormuksen tulivuoreen ja näät kuinka se laskeutuu hehkuvaan laavamereen.\n'
                      f'Hetken sormus pysyy pinnalla, mutta nopeasti se sulaa ja uppoaa laavaan.\n'
                      f'Päästät huokauksen helpotuksesta ja katsot ylös kuinka taivas kirkastuu.\n'
                      f'Sormuksen vaikutus alkaa jo pikkuhiljaa hiipua maailmasta.\n'
                      f'Uutinen teostasi kulkee läpi maailman nopeasti ja sinusta on tuleva LEGENDA! Maailman väki HURRAA sankaruudellesi!\n')
                print(f'Onneksi olkoon! Seikkailusi kesti {keltainen}{pelaaja.menneet_paivat}{vari_reset} päivää.\n')
                peli_lapi = True

            # Paha lopetus
            if lopetus == '2':

                # Tausta_musiikki vaihtuu
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('aanet/musiikki/paha_loppu.wav'))

                print('Katsot sormusta ja alla hehkuvaa laavamerta. Sormus tarjoaa käyttäjälleen voimaa ja valtaa.\n'
                      'Se houkuttelee sinua ja antaudut sen valtaan.\n'
                      'Laitat sormuksen sormeen ja tunnet kuinka voima alkaa kasvaa sisälläsi.\n'
                      'Mielestäsi sinun tulisi ohjata maailmaa, vai onko se sormuksen vaikutus sinuun\n'
                      'Sormuksen vaikutus maailmaan kasvaa ja uudet kätyrit nousevat sinun komennettavaksi\n'
                      'Uutinen teostasi kulkee läpi maailman nopeasti. Maailman väki on kauhuissaan siitä mitä on luvassa kun uusi sormuksen haltija laskeutuu tulivuoren huipulta.\n')
                print(f'Onneksi olkoon! Maailma on armoillasi! Seikkailusi kesti {keltainen}{pelaaja.menneet_paivat}{vari_reset} päivää.\n')
                peli_lapi = True

        # Jos pelaaja häviää taistelun
        else:
            print(f'Olet epäonnistunut. Gorgon ottaa kuolleen ruumiisi haltuun. Nyt uudella vartalolla hän on vahvempi kuin koskaan ja maailma on hänen armossaan taas.')
            print(f'Seikkailusi kesti {keltainen}{pelaaja.menneet_paivat}{vari_reset} päivää.')

            # Poistetaan tallennus
            kuolema_pelin_poisto(pelaaja)
            break

    # tallennus tietokantaan
    tallennus(pelaaja, inventaario)

    # Jos Gorgon voitetaan pelaajan pisteet tallennetaan pisteet tauluun
    if peli_lapi == True:

        tallennuksen_poisto_ja_pisteet(pelaaja)
        input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')

        # Lopputekstit tulee vain jos peli pelataan läpi.
        for x in open(file="tekstitiedostot/lopputekstit.txt",encoding="utf-8"):
            print(f"{keltainen}{x}{vari_reset}", end="")
        input(f'{keltainen}Paina Enter jatkaaksesi...{vari_reset}\n')
        for x in open(file="aanet/lainatut_aanet.txt",encoding="utf-8"):
            print(f"                            {keltainen}{x}{vari_reset}", end="")
        break
