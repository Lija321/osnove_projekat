from common import konstante
from izvestaji import izvestaji
from karte import karte
from letovi import letovi
from konkretni_letovi import konkretni_letovi
from korisnici import korisnici

import sys
import os

ulogovan=False
aktivni_korisnik={}
svi_letovi=letovi.ucitaj_letove_iz_fajla('./fajlovi/letovi.csv',',')
svi_konkretni_letovi=konkretni_letovi.ucitaj_konkretan_let('./fajlovi/konkretni_letovi.csv',',')
sve_karte=karte.ucitaj_karte_iz_fajla('./fajlovi/karte.csv',',')
svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('./fajlovi/korisnici.csv',',')


def cls():
    os.system('cls')

def unesi(msg):
    ret=str(input(f"{msg} >>"))
    return ret

def linija():
    print('='*30)
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
            pasos=unesi("Pasos")
            drzavljanstvo=unesi("Drzavljanstvo")
            telefon=unesi("Telefon")
            pol=unesi("Pol")
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
            continue
    return

def pregled_nerez_letova():
    pass
def pretraga_letova_submeni():
    pass
def trazenje_10_najjeftinijih_letova_submeni():
    pass
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
    pass

def kreiranje_letova():
    pass

def izmena_letova():
    pass

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
            sys.exit()
        except Exception as msg:
            print(f"Greska kasno uhvacena >> {msg}")
            sys.exit()


if __name__ == '__main__':
    main()


