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
import re

from datetime import datetime,timedelta


ulogovan=False
aktivni_korisnik={}

svi_letovi=letovi.ucitaj_letove_iz_fajla('./fajlovi/letovi.csv',',')
svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('./fajlovi/konkretni_letovi.csv',',')
sve_karte=karte.ucitaj_karte_iz_fajla('./fajlovi/karte.csv',',')
svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('./fajlovi/korisnici.csv',',')
svi_modeli=model_aviona.ucitaj_modele_aviona('./fajlovi/modeli.csv',',')


def sacuvaj_sve():
    if len(sys.argv)>1 and sys.argv[1]=='--test':
        return
    letovi.sacuvaj_letove('./fajlovi/letovi.csv',',',svi_letovi)
    konkretni_letovi.sacuvaj_kokretan_let('./fajlovi/konkretni_letovi.csv',',',svi_konkretni_letovi)
    karte.sacuvaj_karte(sve_karte,'./fajlovi/karte.csv',',')
    korisnici.sacuvaj_korisnike('./fajlovi/korisnici.csv',',',svi_korisnici)
    model_aviona.sacuvaj_modele_aviona('./fajlovi/modeli.csv',',',svi_modeli)

def prijava():
    cls()
    print("Prijava")
    while True:
        try:
            linija()
            #korisnicko_ime=unesi("Korisnicko ime")
            #lozinka=unesi("Lozinka")
            korisnicko_ime="Lija321"
            lozinka='Lisica2003!'
            global aktivni_korisnik
            aktivni_korisnik=korisnici.login(svi_korisnici,korisnicko_ime,lozinka)
            global ulogovan
            ulogovan=True
            cls()
            return
        except Exception as msg:
            print(msg)

def izlazak():
    sacuvaj_sve()
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
            sacuvaj_sve()
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
    lista_letova=letovi.pregled_nerealizoivanih_letova(svi_letovi)
    prikaz_letova(lista_letova)

def pretraga_letova_submeni(kupovina=False):
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


            prikaz_konkretnih_letova(pretrazeni_letovi,svi_letovi)

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
            if sifra_polazisnog_aerodroma is None: sifra_polazisnog_aerodroma=''

            elif not len(sifra_polazisnog_aerodroma)==3 and sifra_polazisnog_aerodroma.isalpha():
                print("Greska u unosenju")
                continue

            sifra_odredisnog_aerodroma = unesi("Odredisni aerodrom").upper()
            if sifra_odredisnog_aerodroma is None: sifra_odredisnog_aerodroma = ''

            elif not len(sifra_odredisnog_aerodroma)==3 and sifra_odredisnog_aerodroma.isalpha():
                print("Greska u unosenju")
                continue


            najjeftinij_letovi=letovi.trazenje_10_najjeftinijih_letova(svi_letovi,sifra_polazisnog_aerodroma,sifra_odredisnog_aerodroma)
            prikaz_letova(najjeftinij_letovi)

    except KeyboardInterrupt:
        return

def fleksibilni_polasci_submeni():
    global svi_konkretni_letovi
    global svi_letovi
    while True:
        try:
            print('Ctrl-C za nazad')
            polaziste=unesi('Polaziste').upper()
            odrediste=unesi('Odrediste').upper()

            datum_polaska=unesi('Datum polaska (dd.mm.yyyy)')
            try:
                datum_polaska = datetime.strptime(datum_polaska, '%d.%m.%Y')
            except ValueError:
                raise Exception("Datum polaska pogresno unet")

            datum_dolaska=unesi('Datum dolaska (dd.mm.yyyy)')
            try:
                datum_dolaska = datetime.strptime(datum_dolaska, '%d.%m.%Y')
            except ValueError:
                raise Exception("Datum dolaska pogresno unet")

            broj_fleksibilnih_dana = unesi('Broj fleksibilnih dana')
            if broj_fleksibilnih_dana.isnumeric(): broj_fleksibilnih_dana=int(broj_fleksibilnih_dana)

            moguci_letovi=letovi.fleksibilni_polasci(svi_letovi,
                                       svi_konkretni_letovi,
                                       polaziste,
                                       odrediste,
                                       datum_polaska,
                                       broj_fleksibilnih_dana,
                                       datum_dolaska)
            prikaz_konkretnih_letova(moguci_letovi,svi_letovi)
        except KeyboardInterrupt:
            return
        except Exception as msg:
            print(msg)
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
    global svi_konkretni_letovi
    slobodna_mesta = svi_konkretni_letovi[sifra_leta]['zauzetost']
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

            #prvi_prolaz=True
            putnici = []
            while True:
                kupac=aktivni_korisnik

                if kupuje_za_sebe:
                    putnici.append(aktivni_korisnik)
                    slobodna_mesta = svi_konkretni_letovi[sifra_leta]['zauzetost']
                    karta,sve_karte=karte.kupovina_karte(sve_karte,svi_konkretni_letovi,sifra_leta,
                                         [putnici[-1]],slobodna_mesta,kupac) #putnici[-1] poslednji dodat
                    kupuje_za_sebe=False
                else:
                    while True:
                        ime=unesi("Korisnicko ime putnika")
                        if not ime in svi_korisnici.keys():
                            print("Korisnik ne postoji")
                            continue
                        break
                    putnik=svi_korisnici[ime]
                    putnici.append(putnik)
                    slobodna_mesta = svi_konkretni_letovi[sifra_leta]['zauzetost']
                    karta,sve_karte = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_leta,
                                                     [putnici[-1]], slobodna_mesta, kupac)  #putnici[-1] poslednji dodat
                    #prvi_prolaz=False

                karte.sacuvaj_karte(sve_karte,'./fajlovi/karte.csv',',')
                print("1. Dodaj putnike 1\n2. Kupi za povezujuci let 2\n x. Kraj kupovine ")
                unos=unesi()
                if unos=='1':
                    continue
                elif unos=='2':
                    kupovin_karte_za_povezan_let(putnici,sifra_leta,kupac)
                    return
                elif unos=='x':
                    return

        except KeyboardInterrupt:
            return
        except Exception as msg:
            print_exception(msg)

def kupovin_karte_za_povezan_let(putnici,sifra_leta,kupac):
    global sve_karte
    global svi_konkretni_letovi
    while True:
        try:
            print("Ctrl-C za nazad")
            moguci_letovi=letovi.povezani_letovi(svi_letovi,
                                                 svi_konkretni_letovi,
                                                 svi_konkretni_letovi[sifra_leta])
            prikaz_konkretnih_letova(moguci_letovi,svi_letovi)
            sifra_sledeceg_leta=unesi("Sifra sledeceg leta")
            if sifra_sledeceg_leta.isnumeric(): sifra_sledeceg_leta=int(sifra_sledeceg_leta)
            else: raise Exception("Sifra leta pogresno uneta")
            slobodna_mesta=svi_konkretni_letovi[sifra_sledeceg_leta]['zauzetost']
            for putnik in putnici:
                karta,sve_karte=karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_sledeceg_leta,
                                                             [putnik], slobodna_mesta, kupac)
            sacuvaj_sve()
            while True:
                print("1. Kupi za povezujuci let 1\n x. Kraj kupovine ")
                unos = unesi()
                if unos == '1':
                    kupovin_karte_za_povezan_let(putnici, sifra_sledeceg_leta, kupac)
                    return
                elif unos == 'x':
                    return
                else:
                    print("Uneta nepostojeca opcija")
            return
        except Exception as msg:
            print(msg)

def check_in_konkretnog_korisnika(sifra):
    global sve_karte
    karta = sve_karte[sifra]
    sifra_leta = karta['sifra_konkretnog_leta']
    konkretan_let = svi_konkretni_letovi[sifra_leta]
    print(f'Biranje mesta za {karta["putnici"][0]["korisnicko_ime"]}')
    matrica = letovi.matrica_zauzetosti(konkretan_let)
    model = svi_letovi[konkretan_let['broj_leta']]['model']
    sedista = model['pozicije_sedista']
    print('Sedista oznacena sa X su zauzeta')
    print_sedista(matrica, sedista)

    while True:
        red = unesi("Izaberi red")
        if not red.isnumeric() or not 0 < int(red) <= len(matrica):
            print("Pogresno unet red")
            continue
        red = int(red)
        pozicija = unesi("Koje sediste").upper()
        if not pozicija in sedista:
            print("Pogresno uneta pozicija")
            continue
        pozicija_int = sedista.index(pozicija)
        if matrica[red - 1][pozicija_int]:
            print("Sediste zauzeto")
            continue
        break

    korisnicki_za_proveri = karta['putnici'][0]
    while True:
        if korisnicki_za_proveri['pasos'] == '':
            pasos = unesi("Pasos")
            if not re.match('[0-9]{9}', pasos):
                print("Pasos pogresno unet")
                continue
        if korisnicki_za_proveri['drzavljanstvo'] == '':
            drzavljantsvo = unesi("Drzavljanstvo").lower()
            if not re.match('^[a-z]+$', drzavljantsvo):
                print('Pogresno uneto drzaljvanstvo')
                continue
        if korisnicki_za_proveri['pol'] == '':
            pol = unesi('Pol')
            if not re.match('^[a-z]+$', pol):  # DANAS SVE MOZE BITI POL
                print("Pol pogresno unet")
                continue
        break

    konkretan_let, karta = letovi.checkin(karta, svi_letovi, konkretan_let, red, pozicija)
    sve_karte[karta['broj_karte']] = karta
    sacuvaj_sve()
    return konkretan_let,karta

def check_in_korisnik(povezujuc=False,**kwargs):
    global sve_karte
    global svi_konkretni_letovi
    putnici_za_checkin=[]
    karte_za_checkin=[]
    if 'putnici' in kwargs.keys():
        putnici_za_checkin=kwargs['putnici']
    if 'karte' in kwargs.keys():
        karte_za_checkin=kwargs['karte']
    cls()
    dozvoljene_karte=karte.pregled_nerealizovanaih_karata(aktivni_korisnik,list(sve_karte.values()))
    dozvoljene_karte=list_to_dict(dozvoljene_karte,'broj_karte')

    #Odabir opcija za kartu
    while True and not povezujuc:
        print("1. Pretrazi karte 1\n2. Odaberi kartu kartu pomocu sifre 2\nx. Nazad x")
        unos = unesi('')
        if unos == '1':
            pregled_nerez_karata()
            break
        elif unos == '2':
            break
        elif unos in ['x','X']:
            return
        else:
            print("Odabrana nepostojuca opcija")
            continue


    while True:

        #Odabir karte
        if not povezujuc:
            if dozvoljene_karte=={}:
                print("Nema vise letova za checkin")
                return

            sifra=unesi("Sifra (x-nazad)")
            if sifra=='x': return
            if not sifra.isnumeric() or not int(sifra) in dozvoljene_karte.keys():
                print("Sifra pogresno uneta")
                continue
            sifra=int(sifra)
            karte_za_checkin.append(sve_karte[sifra])
            putnici_za_checkin.append(aktivni_korisnik)
            konkretan_let, karta = check_in_konkretnog_korisnika(sifra)
            break

        else:
            nova_lista_putnika=[]
            konkretan_let=kwargs['let']
            moguci_letovi=letovi.povezani_letovi(svi_letovi,svi_konkretni_letovi,konkretan_let)
            if moguci_letovi==[]:
                print("Nema vise letova za checkin")
                return
            for putnik in kwargs['putnici']:
                print(f"Putnik koji se chekin-uje: {putnik['korisnicko_ime']}")
                moguce_karte=karte.pregled_nerealizovanaih_karata(putnik,sve_karte.values())
                karte_sifre=[x["sifra_konkretnog_leta"] for x in moguce_karte]
                letovi_sifre=[x["sifra"] for x in moguci_letovi]

                karte_sifre=set(karte_sifre).intersection(set(letovi_sifre))
                karte_za_prikaz=[x for x in moguce_karte if x['sifra_konkretnog_leta'] in karte_sifre]
                prikaz_karata(karte_za_prikaz,svi_letovi,svi_konkretni_letovi)
                karte_za_prikaz=list_to_dict(karte_za_prikaz,'broj_karte')
                while True:
                    sifra = unesi("Sifra (x-preskoci)")
                    if sifra == 'x': break
                    if not sifra.isnumeric() or not int(sifra) in karte_za_prikaz.keys():
                        print("Sifra pogresno uneta")
                        continue
                    sifra=int(sifra)
                    konkretan_let, karta = check_in_konkretnog_korisnika(sifra)
                    break
            break



    while True:
        print("1. Check-in saputnika 1\n2. Check-in za povezujuc let 2\nx. Nazad x")
        unos = unesi('')
        if unos == '1':
            cls()
            sifra_konretnog_leta=karta['sifra_konkretnog_leta']
            kupac=karta['kupac']

            gotovo=False
            while not gotovo:
                moguci_saputnici=[]
                for karta_petlja in sve_karte.values():
                    if karta_petlja['sifra_konkretnog_leta']==sifra_konretnog_leta and karta_petlja['kupac']==kupac and not karta_petlja['putnici'][0] in putnici_za_checkin:
                        moguci_saputnici.append(karta_petlja)

                if moguci_saputnici==[]:
                    print('Nema vise saputnika za dodavanje')
                    break

                prikaz_karata(moguci_saputnici,svi_letovi,svi_konkretni_letovi,True)
                moguci_saputnici=list_to_dict(moguci_saputnici,'broj_karte')
                sifra_saputnika_za_dodavanje=unesi('Broj karte za checkin (x za nazad)')
                if sifra_saputnika_za_dodavanje.lower()=='x':
                    gotovo=True
                    continue
                if not sifra_saputnika_za_dodavanje.isnumeric() or not int(sifra_saputnika_za_dodavanje) in moguci_saputnici.keys():
                    print("Pogresna sifra")
                sifra_saputnika_za_dodavanje=int(sifra_saputnika_za_dodavanje)

                putnici_za_checkin.append(sve_karte[sifra_saputnika_za_dodavanje]['putnici'][0])
                check_in_konkretnog_korisnika(sifra_saputnika_za_dodavanje)


        elif unos == '2':
            check_in_korisnik(povezujuc=True,let=konkretan_let,putnici=putnici_za_checkin)
            return
        elif unos in ['x','X']:
            return
        else:
            print("Odabrana nepostojuca opcija")
            continue



def pregled_nerez_karata():
    nerealizovane_karte=karte.pregled_nerealizovanaih_karata(aktivni_korisnik,list(sve_karte.values()))
    prikaz_karata(nerealizovane_karte,svi_letovi,svi_konkretni_letovi)


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

            sacuvaj_sve()
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
                if not 'zauzetost' in let.keys():
                    letovi.podesi_matricu_zauzetosti(svi_letovi,let)


            sacuvaj_sve()

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

            svi_konkretni_letovi=copy(novi_svi_konkretni_letovi)
            svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, #Pravi nove
                                                                              svi_letovi[broj_leta])
            sacuvaj_sve()
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

def prodaj_karata_submeni():
    pass

def check_in_prodavac():
    pass

def izmena_karte():
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
        print('')
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
        '2': check_in_korisnik,
        '3': pregled_nerez_letova,
        '4':pregled_nerez_karata,
        '5': pretraga_letova_submeni,
        '6': trazenje_10_najjeftinijih_letova_submeni,
        '7': fleksibilni_polasci_submeni,
        '8': odjava,
        'x': izlazak
    }
    while True:
        print('')
        linija()
        print("Glavni meni")
        linija()
        print('Opcije:')
        print('1. Kupi kartu 1\n2. Check-in 2\n3. Pregled nerealizovanih letova 3\n4. Pregled nerealizovanih karata 4')
        print('5. Pretraga letova 5\n6. Trazenje 10 najjeftinijh letova 6\n7. Fleksibilni polasci 7\n8. Odjava 8\nx. Izlaz x')

        user_input = str(input(">>"))

        if user_input in ulogovan_meni_korisnik_dict:
            ulogovan_meni_korisnik_dict[user_input]()
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
        print('')
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
            return

        else:
            print("Odabrali ste nepostojeću opciju")
def ulogovan_meni_prodavac():
    ulogovan_meni_korisnik_dict = {
        '1': pretraga_prodatih_karata_submeni,
        '2': prodaj_karata_submeni,
        '3': check_in_prodavac,
        '4': izmena_karte,
        '5': brisanje_karata,
        '6': pregled_nerez_letova,
        '7': pretraga_letova_submeni,
        '8': trazenje_10_najjeftinijih_letova_submeni,
        '9': fleksibilni_polasci_submeni,
        '10': odjava,
        'x': izlazak
    }

    while True:
        print('')
        linija()
        print("Glavni meni")
        linija()
        print('Opcije:')
        print(
            '1. Pretraga prodatih karata 1\n2. Prodaja karata 2\n3. Check-in 3\n4. Izmena karata 4')
        print('5. Brisanje karata 5\n6. Pregled nerealizovanih letova 6')
        print(
            '7. Pretraga letova 7\n8. Trazenje 10 najjeftinijh letova 8\n9. Fleksibilni polasc 9\n10. Odjava 10\nx. Izlaz x')

        user_input = str(input(">>"))

        if user_input in ulogovan_meni_korisnik_dict:
            ulogovan_meni_korisnik_dict[user_input]()
            return

        else:
            print("Odabrali ste nepostojeću opciju")

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
            print(f"Greska kasno uhvacena >> ",end='')
            print_exception(msg)
            sys.exit()


if __name__ == '__main__':
    main()


