import common.konstante
from common import konstante
from ast import literal_eval

def proveri_pasos(pasos):
    pasos = str(pasos)
    if pasos=="": return False, ""
    if not all(x.isdigit() for x in pasos):#Ako se desi da jedan znak nije cifra
        return True, "Pasoš nebrojevni unos"
    if len(pasos) > 9:
        return True, "Pasoš više od 9 cifara"
    if len(pasos) < 9:
        return True, "Pasoš manje od 9 cifara"

    return False, ""


def proveri_telefon(telefon):
    telefon = str(telefon) #U string za svaki slucaj
    if not all(x.isdigit() for x in telefon):#Ako se desi da jedan znak nije cifra
        return True, "Broj telefona nije validan"
    return False, ""


def proveri_email(unos):
    email,uloga=unos
    if not uloga==konstante.ULOGA_KORISNIK: return False,""
    if ' ' in email: return True,'Ima [space] u mejlu'
    if not '@' in email:
        return True, "Email fali @"
    email = email.split('@')
    email = email[1]
    if email.count('.') != 1:#Ako ima vise poddomena, odnsno tacaka na kraju
        return True, "Email provera greska u podomenima"
    email=email.split('.')
    if email[0]=='' or email[1]=='': return True,'Domen ili poddomen prazan'
    return False, ""


def proveri_nedostajucu_vernost(provera_podaci):
    for key, value in provera_podaci.items():
        if value==None or value=="": return True, f"Provera za nedostajucu vrednost: {key}"
    return False, ""


"""

{'Lija321':{'lozinka':'', ime: str, 
            prezime: str, email: str = None, 
            pasos: str = None, drzavljanstvo: str = None, 
            telefon: str = None, pol: str = None},'Toni03':[]}

Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""


def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    korisnik_podaci = {
        'ime': ime, 'prezime': prezime,
        'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka,
        'email': email,
        'pasos': str(pasos), 'drzavljanstvo': drzavljanstvo,
        'telefon': str(telefon), 'pol': pol,
        'uloga': uloga}

    provera_nedostajanje={'ime': ime, 'prezime': prezime,
        'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka}

    provera_funckije = [[proveri_nedostajucu_vernost, provera_nedostajanje],
                        [proveri_pasos, pasos],
                        [proveri_telefon, telefon],
                        [proveri_email, (email,uloga)]]

    # ZOVE SVAKU OF FUNKCIJA PROVERA I VRACA ERROR
    for provera in provera_funckije:
        fun = provera[0]
        prosledi = provera[1]
        greska, poruka = fun(prosledi)
        if greska: raise Exception(poruka)

    # PROVERA ULOGE
    if not (uloga == konstante.ULOGA_PRODAVAC or uloga == konstante.ULOGA_KORISNIK or uloga == konstante.ULOGA_ADMIN):
        raise Exception("Uloga nije validna")

    if azuriraj: #Ako se menja ime [staro i novo razlicito] i novo vec postoji
        if staro_korisnicko_ime != korisnicko_ime and korisnicko_ime in svi_korisnici:
            raise Exception("Korisničko ime je već zauzeto: očekuje se greška")

        if not staro_korisnicko_ime in svi_korisnici: #Ako to ime ne postoji ne moze se azurirati
            raise Exception("Korisnik ne postoji")

        del svi_korisnici[staro_korisnicko_ime]#Brisi staro
        svi_korisnici[korisnicko_ime] = korisnik_podaci#Dodaj novo

    else: # samo promeni unutar korisnika
        identifiktor = korisnicko_ime
        if identifiktor in svi_korisnici:
            raise Exception("Korisnik vec postoji")
        svi_korisnici[identifiktor] = korisnik_podaci


    return svi_korisnici


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    red_cuvanja=['ime','prezime','korisnicko_ime','lozinka','email','pasos','drzavljanstvo','telefon','pol','uloga']
    if not type(svi_korisnici) is dict:
        raise Exception("Greska: svi_korisnici nije dict")
    with open(putanja, 'w') as f:
        for korisnik in svi_korisnici.values():
            nov_red = ""
            for key in red_cuvanja:
                # Cuva se u datom redosledu
                if key in korisnik.keys():
                    nov_red += str(korisnik[key]).replace(',', '~')
                    nov_red += separator
            nov_red = nov_red[:-1]  # oduzima  se bespotrebni separator
            nov_red += '\n'
            f.write(nov_red)

"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""


def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:

    with open(putanja, 'r') as f:
        korisnici = f.readlines()

    korisnici_return = {}
    for red in korisnici:
        red = red.rstrip('\n')
        if red == '': continue
        red=red.split(separator)
        korisnik = {}
        red_cuvanja = ['ime', 'prezime', 'korisnicko_ime', 'lozinka', 'email', 'pasos', 'drzavljanstvo', 'telefon',
                       'pol', 'uloga']
        for i,key in enumerate(red_cuvanja):
            korisnik[key]=red[i]


        korisnici_return[korisnik['korisnicko_ime']]= korisnik

    return korisnici_return


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""  # GOTOVO


def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    try:
        korisnik_podaci = svi_korisnici[korisnicko_ime] #ako korisnicko  ime nepostoji baci ce exception koji keyerror
        if korisnik_podaci["lozinka"] == lozinka:
            return korisnik_podaci
        else:
            raise Exception("Login pogrešna lozinka")
    except KeyError:
        # print("Korisnik nije pronadjen")
        raise Exception("Korisnicko ime ne postoji")

"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    print(f"{korisnicko_ime} uspesno odjavljen")
    return

if __name__ == "__main__":
   pass
