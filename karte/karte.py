import json

import common.konstante
from common import konstante
from functools import reduce
from datetime import datetime
import csv
from ast import literal_eval
from copy import copy
from letovi import letovi

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
) ->  (dict, dict):
    if not sifra_konkretnog_leta in svi_konkretni_letovi:
        raise Exception("Konkretan let ne postoji")

    if not kupac['uloga']==konstante.ULOGA_KORISNIK:
        raise Exception("Neispravna uloga kupca")

    ima_slobodno_mesto=False
    broj_putnika=len(putnici)
    broj_slobodnih_mesta=0
    for red in slobodna_mesta:
        if False in red:
            broj_slobodnih_mesta+=1
    ima_slobodno_mesto= broj_putnika<=broj_slobodnih_mesta
    if ima_slobodno_mesto==False:
        raise Exception("Nema slobodnih mesta")

    #postavljanje broja karte
    global sledeci_broj_karte
    sledeci_broj_karte=sledeci_broj_karte_set(sve_karte)
    broj_karte=sledeci_broj_karte



    #if datum_prodaje=="": datum_prodaje=datetime.now()


    karta = {
        "broj_karte": broj_karte,
        "putnici": putnici,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "status": common.konstante.STATUS_NEREALIZOVANA_KARTA,
        "kupac":kupac,
        "obrisana": False
    }

    if 'datum_prodaje' in kwargs.keys():
        karta['datum_prodaje']=kwargs['datum_prodaje'] #Ako nisu prazni dodaj ih
    if 'prodavac' in kwargs.keys():
        prodavac=kwargs['prodavac']
        if not prodavac['uloga']==konstante.ULOGA_PRODAVAC:
            raise Exception("Samo prodavac moze da proda kartu")
        karta["prodavac"]=kwargs['prodavac']

    sve_karte[karta['broj_karte']]=karta

    return karta,sve_karte

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
                karte_ret.append(copy(karta))
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
    red_cuvanja=['broj_karte','putnici','sifra_konkretnog_leta','status','kupac','obrisana','sediste']
    with open(putanja,'w') as f:
        for karta in sve_karte.values():
            nov_red = ""
            for key in red_cuvanja:
                # Cuva se u datom redosledu
                if key in karta.keys():
                    dodatak = str(karta[key]).replace(',', '~')
                    nov_red +=dodatak
                    nov_red += separator
            nov_red = nov_red[:-1]  # oduzima  se bespotrebni separator
            nov_red += '\n'
            f.write(nov_red)
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
        red=red.split(separator)
        karta={}
        karta['broj_karte']=int(red[0])
        red[1]=red[1].replace('~',',')
        karta['putnici']=literal_eval(red[1])
        karta['sifra_konkretnog_leta']=int(red[2])
        karta['status']=red[3]
        red[4]=red[4].replace('~',',')
        karta['kupac']=literal_eval(red[4])
        karta['obrisana']=literal_eval(red[5])
        if len(red)>6:
            karta['sediste']=red[6]

        karte_ret[karta['broj_karte']]=karta


    return karte_ret


"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska: datetime=None,
    sediste=None
) -> dict:
    if not broj_karte in sve_karte.keys(): raise Exception("Nepostojeci broj karte")
    karta_za_menjanje=copy(sve_karte[broj_karte])

    if not nova_sifra_konkretnog_leta is None:
        if not nova_sifra_konkretnog_leta in svi_konkretni_letovi.keys(): raise Exception("Nov izabran let ne postoji")
        karta_za_menjanje['sifra_konkretnog_leta']=nova_sifra_konkretnog_leta

    if not nov_datum_polaska is None: #Pitaj ovo
        pass
    if not sediste is None:
        karta_za_menjanje['sediste']=sediste




    sve_karte[broj_karte]=karta_za_menjanje
    return sve_karte


"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: str="",
                             korisnicko_ime_putnika: str="")->list:
    polaziste_prazno=polaziste==''
    odrediste_prazno=odrediste==''
    datum_dolaska_prazan=datum_dolaska==''
    datum_polaska_prazan=datum_polaska==''
    korisnicko_ime_putnika_prazno=korisnicko_ime_putnika==''

    karte_ret=[]
    for karta in sve_karte.values():
        konkretan_let=svi_konkretni_letovi[karta['sifra_konkretnog_leta']]
        let=svi_letovi[konkretan_let['broj_leta']]

        if polaziste_prazno: polaziste=let['sifra_polazisnog_aerodroma']
        if odrediste_prazno: odrediste=let['sifra_odredisnog_aerodorma']
        if datum_polaska_prazan: datum_polaska=konkretan_let['datum_i_vreme_polaska']
        if datum_dolaska_prazan: datum_dolaska=konkretan_let['datum_i_vreme_dolaska']
        if korisnicko_ime_putnika_prazno: korisnicko_ime_putnika=karta['putnici'][0]['korisnicko_ime']

        if polaziste==let['sifra_polazisnog_aerodroma'] and \
            odrediste==let['sifra_odredisnog_aerodorma'] and \
            datum_polaska==konkretan_let['datum_i_vreme_polaska'] and \
            datum_dolaska==konkretan_let['datum_i_vreme_dolaska'] and \
            korisnicko_ime_putnika==karta['putnici'][0]['korisnicko_ime']:
            karte_ret.append(copy(karta))
    return karte_ret
if __name__ == '__main__':
    pass