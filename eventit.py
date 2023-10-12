import random
import colorama
from colorama import Fore
from colorama import Style


# TEKSTIVÄRIT:
punainen = colorama.Fore.LIGHTRED_EX
keltainen = colorama.Fore.LIGHTYELLOW_EX
syaani = colorama.Fore.LIGHTCYAN_EX
magenta = colorama.Fore.LIGHTMAGENTA_EX
vihrea = colorama.Fore.LIGHTGREEN_EX
sininen = colorama.Fore.LIGHTBLUE_EX
vari_reset = Style.RESET_ALL



def event_valitsin(pelaaja):
    if int(pelaaja.sijainti) == 1:
        uudentoivon_kyla_event(pelaaja)

    elif int(pelaaja.sijainti) == 2:
        ruoholaakso_event(pelaaja)

    elif int(pelaaja.sijainti) == 3:
        velhotorni_event()

    elif int(pelaaja.sijainti) == 4:
        varisrame_event(pelaaja)

    elif int(pelaaja.sijainti) == 5:
        noitametsa_event(pelaaja)

    elif int(pelaaja.sijainti) == 6:
        sammakkojarvi_event(pelaaja)

    elif int(pelaaja.sijainti) == 7:
        suurentarmon_kaupunki_event(pelaaja)

    elif int(pelaaja.sijainti) == 8:
        hiisisuo_event(pelaaja)

    elif int(pelaaja.sijainti) == 9:
        peikkoluola_event(pelaaja)

    return


def uudentoivon_kyla_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Olet aina tervetullut kotikylääsi!\n'
              'Ystäväsi haluavat kuulla kaiken matkaltasi.\n'
              f'Tarinoidessasi unohdat ajantajun ja matkaasi lisätään {punainen}yksi{vari_reset} päivä.\n')
        pelaaja.menneet_paivat += 1

    return


def ruoholaakso_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Matkallesi on kaatunut 300 vuotta vanha puu.\n')
        vaihtoehto = input(f'{vihrea}1. Otatko kiertoreitin? {vari_reset}{punainen}2. Yritätkö mennä puun yli?:{vari_reset} \n')

        while True:
            if vaihtoehto == '1':
                print(f'Kiertoreitti kestää oletettua kauemmin. Päiviä tulee {punainen}1{vari_reset} lisää\n')
                pelaaja.menneet_paivat += 1
                break

            if vaihtoehto == '2':
                print('Olet nokkela! Pääset puun yli helposti.\n')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def velhotorni_event():
    event_nro = random.randint(1, 1)

    if event_nro == 1:

        print('Löydät kasan eliksiirejä')
        vaihtoehto = input(f'{vihrea}1. Otatko eliksiirit mukaasi?{vari_reset} {punainen}2. Jätätkö ne siihen?{vari_reset}: \n')

        while True:
            if vaihtoehto == '1':
                print('Käsissäsi on liikaa eliksiirejä.\n'
                      'Eliksiirit kaatuvat ja hajoavat maahan\n')
                break

            if vaihtoehto == '2':
                print('Päätät jättää eliksiirit paikalleensa. Jatkat matkaa\n')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def varisrame_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Löydät rämeiköstä nuhjaantuuneen loitsukirjan.\n'
              'Se houkuttelee sinua.\n')
        vaihtoehto = input(f'{vihrea}1. Nappaa loitsukirja ja tutki sitä{vari_reset}, {punainen}2. jätä loitsu kirja rämeikköön{vari_reset}: ')

        while True:
            if vaihtoehto == '1':
                print('Päätät tutkia loitsukirjaa.\n'
                      'Se avautuu kuin itsestään ja tunnet kuinka saat siitä voimaa\n'
                      f'{magenta}Taitopisteeesi{vari_reset} palautuvat täysille!\n')
                pelaaja.taitopiste = pelaaja.max_taitopiste
                break

            if vaihtoehto == '2':
                print('Loitsukirja jää makaamaan maahan ja jatkat matkaasi.')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def noitametsa_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Noitametsän noidat kutsuvat sinut luoksensa Noitataloon.\n')
        vaihtoehto = input(f'{vihrea}1. Menetkö Noitataloon?{vari_reset} {punainen}2. Kieltäydytkö kutsusta?{vari_reset}:')

        while True:
            if vaihtoehto == '1':
                pelaaja.hp = pelaaja.maxhp
                print(f'Noidat ovat anteliaita ja saat juoda heidän taikalientään. Saat {punainen}MAX HP{vari_reset}!\n')
                break

            if vaihtoehto == '2':
                print('Noidat ovat pelottavia. Jatkat matkaa.\n')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def sammakkojarvi_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Saavut salaperäisen Sammakkojärven rannalle.\n'
              'Järvestä kohoaa outoja ääniä ja näet, että järvi on täynnä sammakoita.\n'
              'Yksi sammakoista pyytää suukkoa. Annatko sammakolle suukon?\n')
        vaihtoehto = input(f'{vihrea}1. Anna suukko{vari_reset}, {punainen}2. Kieltäydy tarjouksesta kohteliaasti{vari_reset}: ')
        while True:
            if vaihtoehto == '1':
                print('Suostut antamaan sammakolle suukon, ja yhtäkkiä sammakko muuttuu kauniiksi prinssiksi!\n'
                      'Pelastit prinssin elämän ja löysit oman seikkailurakkautesi!\n'
                      f'Rakkaudesta täyttyneenä saat {punainen}MAX HP{vari_reset}\n')
                pelaaja.hp = pelaaja.maxhp
                break

            if vaihtoehto == '2':
                print('Päätät olla suutelematta sammakkoa ja jatkat matkaasi.\n')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def suurentarmon_kaupunki_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Kävelet kaupungilla ja huomaat torilla kauppiaan.\n'
              'Kauppiaalla on häkissä lohikäärmeen poikasia\n'
              'Voisit yrittää avata häkin salaa ja päästää poikaset vapaaksi\n')
        vaihtoehto = input(f'{vihrea}1. Päästätkö lohikäärmeet vapaaksi?{vari_reset} {punainen}2. Jätätkö ne häkkiin?{vari_reset}: ')

        while True:
            if vaihtoehto == '1':
                print('Livahdat kojun taakse ja tiirikoit poikasten häkin auki.\n'
                      'Poikaset alkavat riehua torilla ja aiheuttavat kaaosta.\n'
                      f'Mellakassa kaadut ja menetät {punainen}3 HP{vari_reset}\n')
                pelaaja.hp -= 3
                break

            if vaihtoehto == '2':
                print('Jätät lohikäärmeet oman onnensa nojaan. Jatkat matkaa.\n')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def hiisisuo_event(pelaaja):

    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Jatkat matkaasi ja saavut säteilevään hiisisuohon.\n'
              'Suo on täynnä kristallinkirkkaita kukkasia.\n'
              'Yhtäkkiä huomaat, että pensaan takana on kaksi pientä keijua\n')

        vaihtoehto = input(f'{vihrea}1. Lähesty keijuja varovasti{vari_reset}, {punainen}2. Yritä piiloutua ja kiertää keijut{vari_reset}: ')

    while True:
        if vaihtoehto == '1':

            print('Keijut tulevat iloisesti luoksesi ja kertovat sinulle tarinoita ja lauluja.\n'
                  'He tarjoavat sinulle myös taikajuomaa, joka tekee sinusta pienemmän\n'
                  'ja saat liidellä keijujen kanssa kukkien loistossa. Päiväsi muuttuu taianomaiseksi!\n')
            break


        if vaihtoehto == '2':
            print('Yrität kiertää keijut, mutta ne havaitsevat sinut.\n'
                  'Keijut tönäisevät sinut suohon! Olet jumissa suossa yön yli.\n'
                  f'Matkaasi lisätään {punainen}1{vari_reset} päivä\n')
            pelaaja.menneet_paivat += 1
            break

        else:
            vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return


def peikkoluola_event(pelaaja):
    event_nro = random.randint(1, 1)

    if event_nro == 1:
        print('Kävelet rauhallista polkua pitkin kohti Peikkoluolaa.\n'
              'Astelet sillan yli kun kuulet jonkun kutsuvan sinua.\n')

        vaihtoehto = input(f'{vihrea}1. Tutki rohkeasti, kuka on sillan alla{vari_reset}, {punainen}2. Jatka matkaasi kohti Peikkoluolaa{vari_reset}: ')
        while True:
            if vaihtoehto == '1':
                print('Kurkkaat rohkeasti sillan alle ja tunnet nopean riuhtaisun.\n'
                      'Vihreä peikko vetää sinut sillan alle ja antaa sinulle selkäsaunan.\n')
                pelaaja.hp -= 3
                print(f'Menetät {punainen}3 HP{vari_reset}')
                break

            if vaihtoehto == '2':
                print('Jatkat matkaasi kohti Peikkoluolaa...\n')
                break

            else:
                vaihtoehto = input(f'Valitse {vihrea}1{vari_reset}/{punainen}2{vari_reset}: ')

    return

