import json

import common.konstante
from common import konstante
from functools import reduce
from datetime import datetime
import csv
from ast import literal_eval

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def sledeci_broj_karte(sve_karte:dict):
    ids=sve_karte.keys()
    ids=list(ids)
    ids.sort()
    if len(ids)>0: id=ids[-1]+1
    else: id=0

    return id


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
        if 'X' in red:
            ima_slobodno_mesto=True
            break
    if slobodna_mesta==[]:
        ima_slobodno_mesto=True

    if ima_slobodno_mesto==False:
        raise Exception("Nema slobodnih mesta")

    broj_karte=sledeci_broj_karte(sve_karte)
    prodavac=kwargs['prodavac']
    datum_prodaje=kwargs['datum_prodaje']

    if datum_prodaje=="": datum_prodaje=datetime.now()


    karta = {
        "broj_karte": broj_karte,
        "putnici": putnici,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "status": common.konstante.STATUS_NEREALIZOVANA_KARTA,
        "kupac":kupac,
        #"obrisana": False,
        "datum_prodaje": datum_prodaje
    }

    if prodavac!="": karta["prodavac"]=prodavac

    sve_karte[karta['broj_karte']]=karta
    return karta
    #return sve_karte

"""
Vraća sve nerealizovane karte za korisnika u listi.
"""
def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: dict) -> list:
    karte_ret=[]
    #for karta in sve_karte.values():
    for karta in sve_karte:
        print(json.dumps((karta)))
        if karta['kupac']==korisnik and karta['status']==common.konstante.STATUS_NEREALIZOVANA_KARTA:
            karte_ret.append(karta)
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
    if korisnik['uloga']==common.konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
    else:
        sve_karte[broj_karte]['obrisana']=True
    return sve_karte

"""
Funkcija koja čuva sve karte u fajl na zadatoj putanji.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja,'w') as f:
        for karta in sve_karte.values():
            red=str(karta)+'\n'
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
        karta=literal_eval(red)

        karte_ret[karta['broj_karte']]=karta


    return karte_ret



if __name__ == '__main__':
    pass