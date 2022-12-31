from common import konstante
from izvestaji import izvestaji
from karte import karte
from letovi import letovi
from konkretni_letovi import konkretni_letovi
from korisnici import korisnici
from model_aviona import model_aviona
from aerodromi import aerodromi
from meni.meni import *

import sys
import os
import platform
from ast import literal_eval

from datetime import datetime,timedelta

def sacuvaj_zauzetost(putanja,sva_zauzetost):
    with open(putanja,'w') as f:
        for zauzetost in sva_zauzetost.values():
            red=str(zauzetost)+'\n' #cuva red po red kao string
            f.write(red)

def ucitaj_zuzetost(putanja: str) -> dict:
    with open(putanja, 'r') as f:
        sva_zazuetost = f.readlines()
    zauzetost_ret={}
    for red in sva_zazuetost:
        red=red.rstrip('\n')
        if red == '': continue
        zauzetost=literal_eval(red)# safe eval svakog reda
        zauzetost_ret[zauzetost['sifra']]=zauzetost
    return zauzetost_ret


ulogovan=False
aktivni_korisnik={}

svi_letovi=letovi.ucitaj_letove_iz_fajla('./fajlovi/letovi.csv',',')
svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('./fajlovi/konkretni_letovi.csv',',')
sve_karte=karte.ucitaj_karte_iz_fajla('./fajlovi/karte.csv',',')
svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('./fajlovi/korisnici.csv',',')
svi_modeli=model.ucitaj_modele('./fajlovi/modeli.csv',',')

sva_zauzetost=ucitaj_zuzetost('./fajlovi/zauzetost.csv')

da_ne_dict={
        "da":True,
        'ne':False,
        "y":True,
        'n':False,
        'yes':True,
        'no':False,
        'd':True,
        'n':False,
        'true':True,
        'false':False
    }

def prijava():
    cls()
    print("Prijava")
    while True:
        try:
            linija()
            korisnicko_ime=unesi("Korisnicko ime")
            lozinka=unesi("Lozinka")
            #korisnicko_ime="Lija321"
            #lozinka='Lisica2003!'
            global aktivni_korisnik
            aktivni_korisnik=korisnici.login(svi_korisnici,korisnicko_ime,lozinka)
            global ulogovan
            ulogovan=True
            return
        except Exception as msg:
            print(msg)

def izlazak():
    print("Doviđenja!!!")
    sys.exit()

def registracija():
    cls()
    azuriraj=False
    uloga=konstante.ULOGA_KORISNIK
    uspelo=False
    while not uspelo:
        try:
            print("\nCtrl-C za unosenje ispocetka")
            korisnicko_ime=unesi("Korisnicko ime")
            lozinka=unesi("Lozinka")
            ime=unesi("Ime")
            prezime=unesi("Prezime")
            email=unesi("Email")
            pasos=unesi("Pasos (opciono)")
            drzavljanstvo=unesi("Drzavljanstvo (opciono)")
            telefon=unesi("Telefon")
            pol=unesi("Pol (opciono)")
            global svi_korisnici
            svi_korisnici=korisnici.kreiraj_korisnika(svi_korisnici,azuriraj,uloga,'',
                                                      korisnicko_ime,lozinka,ime,prezime,email,
                                                      pasos,drzavljanstvo,telefon,pol)
            global ulogovan
            ulogovan=True
            global aktivni_korisnik
            aktivni_korisnik=svi_korisnici[korisnicko_ime]
            uspelo=True
        except KeyboardInterrupt:
            print('')
            linija()
            print('1. Kreni ispocetka [enter]\nx. Nazad x')
            unos=unesi('')
            if unos=='x': return
            continue
        except Exception as msg:
            print(msg)
            continue
    return

def pregled_nerez_letova():
    global svi_letovi
    letovi.pregled_nerealizovanih_letova(svi_letovi)

def pretraga_letova_submeni(kupovina=False):
    if not kupovina: cls()
    filteri_unos={
        '1': "",
        '2': "",
        '3': "",
        '3': "",
        '4': "",
        '5': "",
        '6': "",
        '7': ""
    }
    filteri_poruka=[
        'Polaziste',
        'Odrediste',
        'Datum polaska (dd.mm.yyyy)',
        'Datum dolaska (dd.mm.yyyy)',
        'Vreme poletanja (hh:mm)',
        'Vreme sletanja (hh:mm)',
        'Prevoznik'
    ]
    while True:
        try:
            print("Ctrl-C za nov pokusaj")
            print('Odaberite filtere:')
            print('1. Polaziste 1\n2. Odrediste 2\n3. Datum polaska 3\n4. Datum dolaska 4')
            print('5. Vreme poletanja 5\n6. Vreme sletanja 6\n7. Prevoznik 7\nx. Nazad x')
            odabrani_filteri=unesi("Odaberite filtere npr[157]")
            if 'x' in odabrani_filteri: return
            odabrani_filteri=remove_duplicate(odabrani_filteri)

            for x in odabrani_filteri:
                if not x in filteri_unos.keys(): raise Exception(f'Odabran nevalidan filter {x}')
                filteri_unos[x]=unesi(filteri_poruka[int(x)-1])

            if not filteri_unos['3']=='':
                try:
                    filteri_unos['3'] = datetime.strptime(filteri_unos['3'], '%d.%m.%Y')
                except ValueError:
                    raise Exception("Datum pocetka operativnosti pogresno unet")

            if not filteri_unos['4']=='':
                try:
                    filteri_unos['4'] = datetime.strptime(filteri_unos['4'], '%d.%m.%Y')
                except ValueError:
                    raise Exception("Datum pocetka operativnosti pogresno unet")

            pretrazeni_letovi=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,
                                             filteri_unos['1'].upper(),
                                             filteri_unos['2'].upper(),
                                             filteri_unos['3'],
                                             filteri_unos['4'],
                                             filteri_unos['5'],
                                             filteri_unos['6'],
                                             filteri_unos['7'])
            if not kupovina:
                formatiranje = ['Broj leta', 'Polaziste', 'Odrediste', 'Vreme sletanja', 'Vreme poletanja',
                                'Sletanje sutra',
                                'Prevoznik','Cena','Datum polaska','Datum dolaska']
                keys = ['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
                        'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik',
                        'cena','datum_i_vreme_polaska','datum_i_vreme_dolaska']
            else:
                formatiranje = ['Sifra leta', 'Polaziste', 'Odrediste', 'Vreme sletanja', 'Vreme poletanja',
                                'Sletanje sutra',
                                'Prevoznik', 'Cena', 'Datum polaska', 'Datum dolaska']
                keys = ['sifra', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
                        'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik',
                        'cena', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska']
            podaci = []
            for let in pretrazeni_letovi:
                lista_leta = konkretan_let_format_za_prikaz(let, keys,svi_letovi)
                podaci.append(lista_leta)
            tabelarni_prikaz(podaci, formatiranje, 15)
            if kupovina: return

        except KeyboardInterrupt:
            pass
        except Exception as msg:
            print(msg)

def trazenje_10_najjeftinijih_letova_submeni():
    cls()
    try:
        print("Ctrl-C za nazad")
        while True:
            sifra_polazisnog_aerodroma = unesi("Polazisni aerodrom").upper()
            if not len(sifra_polazisnog_aerodroma)==3 and len(sifra_odredisnog_aerodroma)==3:
                print("Greska u unosenju")
                continue
            sifra_odredisnog_aerodroma = unesi("Odredisni aerodrom").upper()
            if not sifra_polazisnog_aerodroma.isalpha() and sifra_odredisnog_aerodroma.isalpha():
                print("Greska u unosenju")
                continue
            najjeftinij_letovi=letovi.trazenje_10_najjeftinijih_letova(svi_letovi,sifra_polazisnog_aerodroma,sifra_odredisnog_aerodroma)
            formatiranje=['Broj leta','Polaziste','Odrediste','Vreme sletanja','Vreme poletanja','Sletanje sutra',
                          'Prevoznik','Cena']
            keys=['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
                  'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik','cena']
            podaci=[]
            for let in najjeftinij_letovi:
                lista_leta=let_format_za_prikaz(let,keys)
                podaci.append(lista_leta)
            tabelarni_prikaz(podaci,formatiranje,15)

    except KeyboardInterrupt:
        return

def fleksibilni_polasci_submeni():
    pass
def kupovina_karata_submeni():
    cls()
    while True:
        print("1. Pretrazi letove 1\n2. Kupi kartu pomocu sifre 2\nx. Nazad x")
        unos=unesi('')
        if unos=='1':
            pretraga_letova_submeni(kupovina=True)
            continue
        elif unos=='2':
            kupovina_karte()
        elif unos=='x':
            return
        else:
            print("Odabrana nepostojuca opcija")
            continue
        return

def ima_li_slobodnih(sifra_leta):
    slobodna_mesta = sva_zauzetost[sifra_leta]['matrica']
    broj_slobodnih_mesta = 0
    for red in slobodna_mesta:
        for mesto in red:
            if mesto == False: broj_slobodnih_mesta += 1
    if broj_slobodnih_mesta == 0:
        raise Exception('Nema slobodnih mesta')
    print(f'Broj slobodnih mesta >> {broj_slobodnih_mesta}')
def kupovina_karte():
    global sve_karte
    while True:
        print('Ctrl-C za nazad')
        try:
            sifra_leta=unesi("Sifra leta")
            if not sifra_leta.isnumeric():
                print("Neispravno uneta sifra")
                continue

            sifra_leta=int(sifra_leta)
            if not sifra_leta in svi_konkretni_letovi.keys():
                print("Nepostojeca sifra")
            ima_li_slobodnih(sifra_leta)

            kupuje_za_sebe=True
            while True:
                kupuje_za_sebe=unesi("Da li kupujete kartu za sebe? (da/ne)").lower()
                if not kupuje_za_sebe in da_ne_dict.keys():
                    print("Neispravan unos")
                    continue
                kupuje_za_sebe=da_ne_dict[kupuje_za_sebe]
                break

            prvi_prolaz=True
            putnici = []
            while True:
                kupac=aktivni_korisnik

                if kupuje_za_sebe:
                    putnici.append(aktivni_korisnik)
                    slobodna_mesta = sva_zauzetost[sifra_leta]['matrica']
                    sve_karte=karte.kupovina_karte(sve_karte,svi_konkretni_letovi,sifra_leta,
                                         putnici[-1],slobodna_mesta,kupac) #putnici[-1] poslednji dodat
                    kupuje_za_sebe=False
                else:
                    ime=unesi("Ime putnika")
                    prezime=unesi("Prezime putnika")
                    putnik={'ime':ime,'prezime':prezime}
                    putnici.append(putnik)
                    slobodna_mesta = sva_zauzetost[sifra_leta]['matrica']
                    sve_karte = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_leta,
                                                     putnici[-1], slobodna_mesta, kupac)
                    prvi_prolaz=False

                print("1. Dodaj putnike 1\n2. Kupi za povezujuci let 2\n x. Kraj kupovine ")
                unos=unesi()
                if unos=='1':
                    continue
                elif unos=='2':
                    nadji_povezujuc(putnici,svi_konkretni_letovi[sifra_leta],kupac)
                elif unos=='x':
                    return




        except KeyboardInterrupt:
            return
        except Exception as msg:
            print(msg)

def nadji_povezujuc(putnici,prosli_let,kupac):
    global svi_letovi
    global svi_konkretni_letovi
    time_delta=timedelta(minutes=120)
    polaziste=svi_letovi[prosli_let['broj_leta']]["sifra_odredisnog_aerodorma"]
    datum_polaska=prosli_let['datum_i_vreme_dolaska']
    vreme_donja_granica = datum_polaska
    vreme_goranja_granica = datum_polaska + time_delta
    letovi_moguci=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,'',vreme_donja_granica)
    letovi_moguci+=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi,polaziste,'',vreme_goranja_granica)

    temp_letovi=letovi_moguci[:]
    letovi_moguci=[]
    for let in temp_letovi:
        datum_i_vreme_leta=let['datum_i_vreme_polaska']
        if vreme_donja_granica <= datum_i_vreme_leta <= vreme_goranja_granica:
            letovi_moguci.append(dict(let))

    while True:
        pass
def check_in():
    pass
def pregled_nerez_karata():
    pass
def odjava():
    global aktivni_korisnik
    korisnici.logout(aktivni_korisnik['korisnicko_ime'])
    global ulogovan
    ulogovan=False
    aktivni_korisnik={}
    cls()
    return

def pretraga_prodatih_karata_submeni():
    pass

def registracija_novih_prodavaca_submeni():
    cls()
    azuriraj = False
    uloga = konstante.ULOGA_PRODAVAC
    uspelo = False
    while True:
        try:
            print("\nCtrl-C za unosenje ispocetka")
            korisnicko_ime = unesi("Korisnicko ime")
            lozinka = unesi("Lozinka")
            ime = unesi("Ime")
            prezime = unesi("Prezime")
            global svi_korisnici
            svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, azuriraj, uloga, '',
                                                        korisnicko_ime, lozinka, ime, prezime)

            cls()
            return

        except KeyboardInterrupt:
            print('')
            linija()
            print('1. Kreni ispocetka [enter]\nx. Nazad x')
            unos = unesi('')
            if unos == 'x': return

        except Exception as msg:
            print(msg)
    return

def kreiranje_letova():
    global svi_konkretni_letovi
    global svi_letovi
    cls()
    dan_to_const={
        'pon':konstante.PONEDELJAK,
        'uto':konstante.UTORAK,
        'sre':konstante.SREDA,
        'cet':konstante.CETVRTAK,
        'čet':konstante.CETVRTAK,
        'pet':konstante.PETAK,
        'sub':konstante.SUBOTA,
        'ned':konstante.NEDELJA
    }

    while True:
        try:
            print("\nCtrl-C za unosenje ispocetka")

            broj_leta = unesi("Broj leta").upper()

            sifra_polazisnog_aerodroma = unesi("Polazisni aerodrom").upper()
            sifra_odredisnog_aerodroma = unesi("Odredisni aerodrom").upper()

            vreme_poletanja=unesi("Vreme poletanja (hh:mm)(00-24)")
            vreme_sletanja = unesi("Vreme sletanja (hh:mm)(00-24)")

            sletanje_sutra=unesi("Sletanje sutra (da/ne)").lower()
            if sletanje_sutra in da_ne_dict: sletanje_sutra=da_ne_dict[sletanje_sutra]
            else: raise Exception('Sletanje sutra pogresno uneto')

            prevoznik=unesi("Prevoznik")

            dani=unesi('Dani [pon,uto,sre,cet,pet,sub,ned]').lower()
            dani=dani.split(',')
            if len(dani)!=len(list(set(dani))): raise Exception("Dani se ponavljaju")
            for i in range(len(dani)):
                if not dani[i] in dan_to_const.keys(): raise Exception(f"Greska u unosenju dana >> {dani[i]}!")
                dani[i]=dan_to_const[dani[i]]

            model=int(unesi("Id modela aviona"))
            model=svi_modeli[model]

            cena=float(unesi("Cena"))

            datum_pocetka_operativnosti=unesi('Datum pocetka operativnosti (dd.mm.yyyy)')
            try:
                datum_pocetka_operativnosti=datetime.strptime(datum_pocetka_operativnosti,'%d.%m.%Y')
            except ValueError:
                raise Exception("Datum pocetka operativnosti pogresno unet")

            datum_kraja_operativnosti = unesi('Datum kraja operativnosti (dd.mm.yyyy)')
            try:
                datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, '%d.%m.%Y')
            except ValueError:
                raise Exception("Datum kraja operativnosti pogresno unet")
                
            '''
            broj_leta="JU50"
            sifra_polazisnog_aerodroma="BEG"
            sifra_odredisnog_aerodroma="NYC"
            vreme_poletanja="12:00"
            vreme_sletanja='23:00'
            sletanje_sutra=False
            prevoznik='AirSerbia'
            dani=[konstante.PONEDELJAK,konstante.PETAK,konstante.NEDELJA]
            model = svi_modeli[123]
            cena=1500.0
            datum_pocetka_operativnosti=datetime(2022,12,1,0,0,0)
            datum_kraja_operativnosti=datetime(2023,5,1,0,0,0)'''

            svi_letovi=letovi.kreiranje_letova(svi_letovi,broj_leta,sifra_polazisnog_aerodroma,sifra_odredisnog_aerodroma,
                                               vreme_poletanja,vreme_sletanja,sletanje_sutra,prevoznik,dani,model,cena,
                                               datum_pocetka_operativnosti,datum_kraja_operativnosti)
            svi_konkretni_letovi=konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi,svi_letovi[broj_leta])

            for let in svi_konkretni_letovi.values():
                red={}
                red['matrica']=letovi.podesi_matricu_zauzetosti(svi_letovi,let)
                red['sifra']=let['sifra']
                sva_zauzetost[let['sifra']]=red

            sacuvaj_zauzetost('./fajlovi/zauzetost.csv',sva_zauzetost)

            konkretni_letovi.sacuvaj_kokretan_let('./fajlovi/konkretni_letovi.csv',',',svi_konkretni_letovi)
            cls()
            return

        except KeyboardInterrupt:
            print('')
            linija()
            print('1. Kreni ispocetka [enter]\nx. Nazad x')
            unos = unesi('')
            if unos == 'x': return
        except Exception as msg:
            print(msg)
    return


def izmena_letova():
    cls()
    global svi_letovi
    global svi_konkretni_letovi
    dan_to_const = {
        'pon': konstante.PONEDELJAK,
        'uto': konstante.UTORAK,
        'sre': konstante.SREDA,
        'cet': konstante.CETVRTAK,
        'čet': konstante.CETVRTAK,
        'pet': konstante.PETAK,
        'sub': konstante.SUBOTA,
        'ned': konstante.NEDELJA
    }
    sletanje_sutra_dict = {
        "da": True,
        'ne': False,
        "y": True,
        'n': False,
        'yes': True,
        'no': False,
        'd': True,
        'n': False,
        'true': True,
        'false': False
    }
    while True:
        try:
            print("\nCtrl-C za unosenje ispocetka")
            broj_leta = unesi("Broj leta za izmenu").upper()
            if  not broj_leta in svi_letovi.keys(): raise Exception("Let ne postoji")

            sifra_polazisnog_aerodroma = unesi("Polazisni aerodrom").upper()
            sifra_odredisnog_aerodroma = unesi("Odredisni aerodrom").upper()

            vreme_poletanja = unesi("Vreme poletanja (hh:mm)(00-24)")
            vreme_sletanja = unesi("Vreme sletanja (hh:mm)(00-24)")

            sletanje_sutra = unesi("Sletanje sutra (da/ne)").lower()
            if sletanje_sutra in sletanje_sutra_dict:
                sletanje_sutra = sletanje_sutra_dict[sletanje_sutra]
            else:
                raise Exception('Sletanje sutra pogresno uneto')

            prevoznik = unesi("Prevoznik")
            dani = unesi('Dani [pon,uto,sre,cet,pet,sub,ned]').lower()
            dani = dani.split(',')
            if len(dani) != len(list(set(dani))): raise Exception("Dani se ponavljaju")
            for i in range(len(dani)):
                if not dani[i] in dan_to_const.keys(): raise Exception(f"Greska u unosenju dana >> {dani[i]}!")
                dani[i] = dan_to_const[dani[i]]

            model = int(unesi("Id modela aviona"))
            model = svi_modeli[model]

            cena = float(unesi("Cena"))

            datum_pocetka_operativnosti = unesi('Datum pocetka operativnosti (dd.mm.yyyy)')
            try:
                datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, '%d.%m.%Y')
            except ValueError:
                raise Exception("Datum pocetka operativnosti pogresno unet")

            datum_kraja_operativnosti = unesi('Datum kraja operativnosti (dd.mm.yyyy)')
            try:
                datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, '%d.%m.%Y')
            except ValueError:
                raise Exception("Datum kraja operativnosti pogresno unet")

            svi_letovi = letovi.izmena_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma,
                                                 sifra_odredisnog_aerodroma,
                                                 vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani,
                                                 model, cena,
                                                 datum_pocetka_operativnosti, datum_kraja_operativnosti)

            novi_svi_konkretni_letovi={}
            for sifra,let in svi_konkretni_letovi.items():#Brise stare
                if not let['broj_leta']==broj_leta: novi_svi_konkretni_letovi[sifra]=let

            svi_konkretni_letovi=novi_svi_konkretni_letovi.copy()
            svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, #Pravi nove
                                                                              svi_letovi[broj_leta])
            konkretni_letovi.sacuvaj_kokretan_let('./fajlovi/konkretni_letovi.csv', ',', svi_konkretni_letovi)
            cls()
            return



        except KeyboardInterrupt:
            print('')
            linija()
            print('1. Kreni ispocetka [enter]\nx. Nazad x')
            unos = unesi('')
            if unos == 'x': return

        except Exception as msg:
            print(msg)
    return

def brisanje_karata():
    pass

def izvestavanje_submeni():
    pass

def neulogovan_meni():
    neulogovan_meni_dict={
        '1':prijava,
        '2':registracija,
        '3':pregled_nerez_letova,
        '4':pretraga_letova_submeni,
        '5':trazenje_10_najjeftinijih_letova_submeni,
        '6':fleksibilni_polasci_submeni,
        'x':izlazak
    }

    while True:
        linija()
        print("Glavni meni")
        linija()
        print('Opcije:')
        print('1. Prijava 1\n2. Registracija 2\n3. Pregled nerealizovanih letova 3')
        print('4. Pretraga letova 4\n5. Trazenje 10 najjeftinijh letova 5\n6. Fleksibilni polasci 6\nx. Izlaz')

        user_input = str(input(">>"))

        if user_input in neulogovan_meni_dict:
            neulogovan_meni_dict[user_input]()
            if user_input == 'x':
                return
            return

        else:
            print("Odabrali ste nepostojeću opciju")

def ulogovan_meni_korisnik():
    ulogovan_meni_korisnik_dict = {
        '1': kupovina_karata_submeni,
        '2': check_in,
        '3': pregled_nerez_letova,
        '4':pregled_nerez_karata,
        '5': pretraga_letova_submeni,
        '6': trazenje_10_najjeftinijih_letova_submeni,
        '7': fleksibilni_polasci_submeni,
        '8': odjava,
        'x': izlazak
    }
    while True:
        linija()
        print("Glavni meni")
        linija()
        print('Opcije:')
        print('1. Kupi kartu 1\n2. Check-in 2\n3. Pregled nerealizovanih letova 3\n4. Pregled nerealizovanih karata 4')
        print('5. Pretraga letova 5\n6. Trazenje 10 najjeftinijh letova 6\n7. Fleksibilni polasci 7\n8. Odjava 8\nx. Izlaz x')

        user_input = str(input(">>"))

        if user_input in ulogovan_meni_korisnik_dict:
            ulogovan_meni_korisnik_dict[user_input]()
            if user_input == 'x':
                return
            return

        else:
            print("Odabrali ste nepostojeću opciju")

def ulogovan_meni_admin():
    ulogovan_meni_korisnik_dict = {
        '1': pretraga_prodatih_karata_submeni,
        '2': registracija_novih_prodavaca_submeni,
        '3': kreiranje_letova,
        '4': izmena_letova,
        '5': brisanje_karata,
        '6': izvestavanje_submeni,
        '7': pregled_nerez_letova,
        '8': pretraga_letova_submeni,
        '9': trazenje_10_najjeftinijih_letova_submeni,
        '10': fleksibilni_polasci_submeni,
        '11': odjava,
        'x': izlazak
    }

    while True:
        linija()
        print("Glavni meni")
        linija()
        print('Opcije:')
        print('1. Pretraga prodatih karata 1\n2. Registracija novih prodavaca 2\n3. Kreiranje letova 3\n4. Izmena letova 4')
        print('5. Brisanje karata 5\n6. Izvestavanje 6\n7. Pregled nerealizovanih letova 7')
        print('8. Pretraga letova 8\n9. Trazenje 10 najjeftinijh letova 9\n10. Fleksibilni polasc 10\n11. Odjava 11\nx. Izlaz x')

        user_input = str(input(">>"))

        if user_input in ulogovan_meni_korisnik_dict:
            ulogovan_meni_korisnik_dict[user_input]()
            if user_input == 'x':
                return
            return

        else:
            print("Odabrali ste nepostojeću opciju")
def ulogovan_meni_prodavac():
    pass

def main():
    while True:
        try:
            global aktivni_korisnik
            if ulogovan:
                if aktivni_korisnik['uloga']==konstante.ULOGA_KORISNIK:ulogovan_meni_korisnik()
                elif aktivni_korisnik['uloga']==konstante.ULOGA_ADMIN:ulogovan_meni_admin()
                elif aktivni_korisnik['uloga']==konstante.ULOGA_PRODAVAC:ulogovan_meni_prodavac()
                else: raise Exception('Uloga aktivnog korisnika neispravna')
            else: neulogovan_meni()
        except KeyboardInterrupt:
            print("")
            izlazak()
        except Exception as msg:
            print(f"Greska kasno uhvacena >> {msg}")
            sys.exit()


if __name__ == '__main__':
    main()


