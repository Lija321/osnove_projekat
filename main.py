from common import konstante
from izvestaji import izvestaji
from karte import karte
from letovi import letovi
from konkretni_letovi import konkretni_letovi
from korisnici import korisnici
from model import model

import sys
import os
import platform

from datetime import datetime

platforma_var=platform.system()

ulogovan=False
aktivni_korisnik={}

svi_letovi=letovi.ucitaj_letove_iz_fajla('./fajlovi/letovi.csv',',')
svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('./fajlovi/konkretni_letovi.csv',',')
sve_karte=karte.ucitaj_karte_iz_fajla('./fajlovi/karte.csv',',')
svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('./fajlovi/korisnici.csv',',')
svi_modeli=model.ucitaj_modele('./fajlovi/modeli.csv',',')



def cls():
    if platforma_var=="Windows":os.system('cls')
    elif platforma_var=="Linux":os.system("clear")
    elif platforma_var.lower()=="darwin":os.system("clear")

def unesi(msg):
    ret=str(input(f"{msg} >>"))
    return ret

def linija(duzina=30):
    print('='*30)

def dict_to_list(dict,keys):
    lista_ret=[]
    for key in keys:
        lista_ret.append(dict[key])
    return lista_ret

def tabelarni_prikaz(podaci, formatiranje, centriranje=15):
    red = '||'
    for parametar in formatiranje:
        red += f'{parametar:^{centriranje}} || '
    print(red)
    print('=' * (len(red) - 1))

    for row in podaci:
        red = '||'
        for item in row:
            item=str(item)
            red += f'{item:^{centriranje}} || '
        print(red)

def dani_to_string(dani):
    dani_dict={
        konstante.PONEDELJAK: 'Pon',
        konstante.UTORAK: 'Uto',
        konstante.SREDA: 'Sre',
        konstante.CETVRTAK: 'Cet',
        konstante.PETAK: 'Pet',
        konstante.SUBOTA: 'Sub',
        konstante.NEDELJA: 'Ned'
    }
    ret=''
    for dan in dani:
        ret+=dani_dict[dan]+','
    ret=ret[:-1]
    return ret

def let_format_za_prikaz(let,keys):
    bool_to_da_ne_dict={True:"Da",False:'Ne'}
    let['model'] = let['model']['naziv']
    let['datum_pocetka_operativnosti'] = let['datum_pocetka_operativnosti'].date()
    let['datum_kraja_operativnosti'] = let['datum_kraja_operativnosti'].date()
    let['dani'] = dani_to_string(let['dani'])
    let['sletanje_sutra']=bool_to_da_ne_dict[let['sletanje_sutra']]
    lista_leta = dict_to_list(let, keys)
    return lista_leta
def prijava():
    cls()
    print("Prijava")
    while True:
        try:
            linija()
            korisnicko_ime=unesi("Korisnicko ime")
            lozinka=unesi("Lozinka")
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
    pass
def pretraga_letova_submeni():
    pass
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
                          'Prevoznik','Dani leta','Cena']
            keys=['broj_leta', 'sifra_polazisnog_aerodroma', 'sifra_odredisnog_aerodorma',
                  'vreme_poletanja', 'vreme_sletanja', 'sletanje_sutra', 'prevoznik',
                  'dani','cena']
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
    sletanje_sutra_dict={
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
    while True:
        try:
            print("\nCtrl-C za unosenje ispocetka")
            broj_leta = unesi("Broj leta").upper()

            sifra_polazisnog_aerodroma = unesi("Polazisni aerodrom").upper()
            sifra_odredisnog_aerodroma = unesi("Odredisni aerodrom").upper()

            vreme_poletanja=unesi("Vreme poletanja (hh:mm)(00-24)")
            vreme_sletanja = unesi("Vreme sletanja (hh:mm)(00-24)")

            sletanje_sutra=unesi("Sletanje sutra (da/ne)").lower()
            if sletanje_sutra in sletanje_sutra_dict: sletanje_sutra=sletanje_sutra_dict[sletanje_sutra]
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


            svi_letovi=letovi.kreiranje_letova(svi_letovi,broj_leta,sifra_polazisnog_aerodroma,sifra_odredisnog_aerodroma,
                                               vreme_poletanja,vreme_sletanja,sletanje_sutra,prevoznik,dani,model,cena,
                                               datum_pocetka_operativnosti,datum_kraja_operativnosti)
            svi_konkretni_letovi=konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi,svi_letovi[broj_leta])
            konkretni_letovi.sacuvaj_kokretan_let('./fajlovi/konkretni_letovi.csv',',',svi_konkretni_letovi)
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
    while True:
        try:
            print("\nCtrl-C za unosenje ispocetka")
            broj_leta = unesi("Broj leta za izmenu").upper()
            if  not broj_leta in svi_letovi.keys(): raise Exception("Let ne postoji")
            sifra_polazisnog_aerodroma = unesi("Polazisni aerodrom").upper()
            sifra_odredisnog_aerodroma = unesi("Odredisni aerodrom").upper()
            vreme_poletanja = unesi("Vreme poletanja (hh:mm)(00-24)")
            vreme_sletanja = unesi("Vreme sletanja (hh:mm)(00-24)")
            sletanje_sutra = bool(unesi("Sletanje sutra (true/false)"))
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

            for sifra,let in svi_konkretni_letovi.items():#Brise stare
                if let['broj_leta']==broj_leta: del svi_konkretni_letovi[sifra]

            svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, #Pravi nove
                                                                              svi_letovi[broj_leta])
            konkretni_letovi.sacuvaj_kokretan_let('./fajlovi/konkretni_letovi.csv', ',', svi_konkretni_letovi)
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
    cls()
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
    cls()
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
    cls()
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


