import common.konstante
from common import konstante


def proveri_pasos(pasos):
    pasos=str(pasos)
    if not all(x.isdigit() for x in pasos):
        return True,"Pasoš nebrojevni string"
    if len(pasos)>9:
        return True,"Pasoš više od 9 cifara"
    if len(pasos)<9:
        return True,"Pasoš manje od 9 cifara"

    return False,""

def proveri_telefon(telefon):
    telefon = str(telefon)
    #print(telefon)
    if not all(x.isdigit() for x in telefon):
        return True, "Broj telefona nije validan"
    return False, ""

def proveri_email(email):
    if not '@' in email:
        return True,"Email provera bez @"
    email=email.split('@')
    email=email[1]
    if email.count('.')!=1:
        return True,"Email provera sa @ ali sa više poddomena"
    return False,""

def proveri_nedostajucu_vernost(provera_podaci: dict):
    for key,value in provera_podaci.items():
        if value is None: return True,f"Provera za nedostajucu vrednost: {key}"
    return False,""


"""

{'Lija321':{'lozinka':'', ime: str, 
            prezime: str, email: str = None, 
            pasos: str = None, drzavljanstvo: str = None, 
            telefon: str = None, pol: str = None},'Toni03':[]}

Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni (ne važi za konverziju brojeva).
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""

def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, korisnicko_ime: str,
                      lozinka: str, ime: str, prezime: str, email: str = None,
                      pasos: str = None, drzavljanstvo: str = None,
                      telefon: str = None, pol: str = None) -> dict:

    korisnik_podaci = {
        'ime': ime,'prezime': prezime,
        'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka,
        'email': email,
        'pasos': str(pasos), 'drzavljanstvo': drzavljanstvo,
        'telefon': str(telefon), 'pol': pol,
        'uloga': uloga}


    provera_funckije=[[proveri_nedostajucu_vernost,korisnik_podaci],
                    [proveri_pasos,pasos],
                      [proveri_telefon,telefon],
                      [proveri_email,email]]

    for provera in provera_funckije:
        fun=provera[0]
        prosledi=provera[1]
        greska,poruka=fun(prosledi)
        if greska: return poruka


    if not (uloga ==konstante.ULOGA_PRODAVAC or uloga==konstante.ULOGA_KORISNIK or uloga==konstante.ULOGA_ADMIN):
        print(uloga, konstante.ULOGA_KORISNIK)
        return "Uloga nije validna"

    if azuriraj:
        identifiktor = korisnik_podaci['korisnicko_ime']
        if not identifiktor in svi_korisnici:
            #print("Korisnik ne postoji")
            return "Korisnik ne postoji"
        svi_korisnici[identifiktor] = korisnik_podaci
    else:
        identifiktor=korisnik_podaci['korisnicko_ime']
        if identifiktor in svi_korisnici:
            #print("Korisnik vec postoji")
            return "Korisnik vec postoji"
        svi_korisnici[identifiktor]=korisnik_podaci
    return svi_korisnici


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
""" #GOTOVO
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    if not type(svi_korisnici) is dict:
        print("Greska")
        return "Greska: svi_korisnici nije dict"

    with open(putanja,'w') as f:
        for korisnik in svi_korisnici.values():
            nov_red=list(korisnik.values())
            nov_red=separator.join(str(val) for val in nov_red)+'\n'
            f.write(nov_red)

"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:  #GOTOVO

    with open(putanja,'r') as f:
        korisnici=f.readlines()

    korisnici_return={}
    for red in korisnici:
        red=red.rstrip('\n')
        red=red.split(separator)
        korisnik_podaci={
                         'ime':red[0] , 'prezime':red[1] ,
                         'korisnicko_ime':red[2],'lozinka':red[3] , 'email':red[4] ,
                         'pasos':int(red[5]), 'drzavljanstvo':red[6],
                         'telefon':int(red[7]),'pol':red[8],
                         'uloga':red[9]}
        korisnici_return[red[2]]=korisnik_podaci
    return korisnici_return


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
""" #GOTOVO
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    try:
        korisnik_podaci=svi_korisnici[korisnicko_ime]
        if korisnik_podaci["lozinka"]==lozinka:
            return korisnik_podaci
        else:
            return "Login pogrešna lozinka"
    except KeyError:
        #print("Korisnik nije pronadjen")
        return "Login nepostojeći"


if __name__=="__main__":
    svi_korisnici=ucitaj_korisnike_iz_fajla('./test_korisnici.csv','|')
    print(svi_korisnici)
    #svi_korisnici={}
    #svi_korisnici=kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, 'Lija321','lisica2003', 'Dejan', 'Lisica', 'lisica.dejan@hotmail.com',123456789, 'Srpsko', '063595793', 'm')
    #sacuvaj_korisnike('./test_korisnici.csv','|',svi_korisnici)
