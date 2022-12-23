from datetime import datetime, date
from functools import reduce

def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: datetime)->list:
    izvestaj_ret=[]
    for karta in sve_karte.values():
        if karta['datum_prodaje']==dan:
            izvestaj_ret.append(karta)
    return izvestaj_ret
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date):
    izvestaj_ret = []
    for karta in sve_karte.values():
        sifra=karta['sifra_konkretnog_leta']
        let=svi_konkretni_letovi[sifra]
        if let['datum_i_vreme_polaska'].date() == dan:
            izvestaj_ret.append(karta)
    return izvestaj_ret

def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str):
    izvestaj_ret = []
    for karta in sve_karte.values():
        if karta['datum_prodaje'] == dan and karta['prodavac']==prodavac:
            izvestaj_ret.append(karta)
    return izvestaj_ret

def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    broj=0
    cena=0
    for karta in sve_karte:
        if karta['datum_prodaje']==dan:
            broj+=1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta=konk_let['broj_leta']
            let=svi_letovi
            cena+=




def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date): #ubc znaci ukupan broj i cena
    pass

def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str): #ubc znaci ukupan broj i cena
    pass

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict)->dict: #ubc znaci ukupan broj i cena
    pass


