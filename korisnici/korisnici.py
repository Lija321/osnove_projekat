import common.konstante
from common import konstante



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

    check_list=[[uloga,korisnicko_ime,lozinka,ime,prezime],[email,pasos,drzavljanstvo,telefon,pol]]


    if all([x is None for x in check_list[1]]):
        korisnik_podaci = {
            'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka, 'ime': ime,
            'prezime': prezime,'uloga': uloga}
    elif all([isinstance(x,str) for x in check_list[0]]):
        korisnik_podaci = {
            'korisnicko_ime': korisnicko_ime, 'lozinka': lozinka, 'ime': ime,
            'prezime': prezime, 'email': email,
            'pasos': pasos, 'drzavljanstvo': drzavljanstvo,
            'telefon': telefon, 'pol': pol,
            'uloga': uloga}

    #Uvesti za gresku
    #if not all([isinstance(x,str) for x in check_list[0]]) or (not all([isinstance(x,str) for x in check_list[1]]) or not all([isinstance(x,None) for x in check_list[0]])):
    #    return "Greska: pogresni tipovi"

    if azuriraj:
        identifiktor = korisnik_podaci['korisnicko_ime']
        if not identifiktor in svi_korisnici:
            print("Korisnik ne postoji")
            return "Korisnik ne postoji"
        svi_korisnici[identifiktor] = korisnik_podaci
    else:
        identifiktor=korisnik_podaci['korisnicko_ime']
        if identifiktor in svi_korisnici:
            print("Korisnik vec postoji")
            return "Korisnik vec postoji"
        svi_korisnici[identifiktor]=korisnik_podaci
    return svi_korisnici


"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
""" #GOTOVO
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    if not type(svi_korisnici) is dict:
        return "Greska: svi_korisnici nije dict"

    with open(putanja,'w') as f:
        for korisnik in svi_korisnici.values():
            nov_red=list(korisnik.values())
            #print(nov_red)
            nov_red=separator.join(nov_red)+'\n'
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
                         'korisnicko_ime':red[0],'lozinka':red[1] , 'ime':red[2] ,
                         'prezime':red[3] , 'email':red[4] ,
                         'pasos':red[5], 'drzavljanstvo':red[6],
                         'telefon':red[7],'pol':red[8],
                         'uloga':red[9]}
        korisnici_return[red[0]]=korisnik_podaci
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
            return "Pogresna sifra"
    except KeyError:
        #print("Korisnik nije pronadjen")
        return "Greska: Korisnik nije pronadjen"


if __name__=="__main__":
    svi_korisnici= ucitaj_korisnike_iz_fajla("./test_korisnici.csv",',')
    svi_korisnici=kreiraj_korisnika(svi_korisnici,False,konstante.ULOGA_PRODAVAC,'Prodavac1','prodajemAVIONE123!','Pera','Peric')
    ret=sacuvaj_korisnike("./test_korisnici.csv",',',svi_korisnici)
    for korisnik in svi_korisnici.values():
        print(korisnik)


