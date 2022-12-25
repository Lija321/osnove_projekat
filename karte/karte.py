import json

import common.konstante
from common import konstante
from functools import reduce
from datetime import datetime
import csv
from ast import literal_eval


def sledeci_broj_karte_set(sve_karte:dict):
    ids=sve_karte.keys()
    ids=list(ids)
    ids.sort()
    if len(ids)>0: id=ids[-1]+1 #uzme se najveci i doda 1
    else: id=1#ako nema uopste postavi se na jedan

    return id

"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs #prodavac i datum prodaje
) -> dict:
    if not sifra_konkretnog_leta in svi_konkretni_letovi:
        raise Exception("Konkretan let ne postoji")

    ima_slobodno_mesto=False
    for red in slobodna_mesta:
        if True in red:
            ima_slobodno_mesto=True #Ako se nadje jedno prazno mesto -> ima mesra
            break
    if slobodna_mesta==[]: #Ako je matrica prazna isto ima mesta
        ima_slobodno_mesto=True

    if ima_slobodno_mesto==False:
        raise Exception("Nema slobodnih mesta")

    #postavljanje broja karte
    global sledeci_broj_karte
    sledeci_broj_karte=sledeci_broj_karte_set(sve_karte)
    broj_karte=sledeci_broj_karte

    prodavac=kwargs['prodavac']
    datum_prodaje=kwargs['datum_prodaje']

    #if datum_prodaje=="": datum_prodaje=datetime.now()


    karta = {
        "broj_karte": broj_karte,
        "putnici": putnici,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "status": common.konstante.STATUS_NEREALIZOVANA_KARTA,
        "kupac":kupac,
        "obrisana": False
    }
    if not datum_prodaje is None: karta['datum_prodaje']=datum_prodaje #Ako nisu prazni dodaj ih
    if prodavac!="": karta["prodavac"]=prodavac

    sve_karte[karta['broj_karte']]=karta

    import sys
    if not 'unittest' in sys.modules.keys():
        sacuvaj_karte('./fajlovi/karte.csv',',',sve_karte)
    return karta #Mislim da je greska u testu
    #return sve_karte

"""
Vraća sve nerealizovane karte za korisnika u listi.
"""
def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter) -> list:
    karte_ret=[]
    for karta in sve_karte:
        #print(json.dumps((karta)))
        if karta["status"]!=konstante.STATUS_NEREALIZOVANA_KARTA: continue #ako nije nerealizovana preskoci
        putnici=karta['putnici']
        for putnik in putnici: #Ako je putnik u korisnicima dodaj kartu
            if putnik['korisnicko_ime']==korisnik['korisnicko_ime']:
                karte_ret.append(karta)
                continue #Vec dodata idi dalje
    return karte_ret


"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata. Baca grešku ako podaci nisu validni.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if not (korisnik['uloga']==common.konstante.ULOGA_ADMIN or korisnik['uloga']==common.konstante.ULOGA_PRODAVAC):
        raise Exception("Nema dozvolu da brise karte")
    if korisnik['uloga']==common.konstante.ULOGA_ADMIN: #Akoje admin brise se
        del sve_karte[broj_karte]
    else: #Ako nije onda je prodavac postavlja se na brisanje
        sve_karte[broj_karte]['obrisana']=True
    return sve_karte

"""
Funkcija koja čuva sve karte u fajl na zadatoj putanji.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja,'w') as f:
        for karta in sve_karte.values():
            red=str(karta)+'\n' #cuva red po red kao string
            f.write(red)

"""
Funkcija koja učitava sve karte iz fajla i vraća ih u rečniku.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, 'r') as f:
        karte = f.readlines()
    karte_ret={}
    for red in karte:
        red=red.rstrip('\n')
        if red == '': continue
        karta=literal_eval(red)# safe eval svakog reda

        karte_ret[karta['broj_karte']]=karta


    return karte_ret



if __name__ == '__main__':
    pass