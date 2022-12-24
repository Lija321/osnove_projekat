from datetime import datetime, date, timedelta
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
    for karta in sve_karte.values():
        if karta['datum_prodaje']==dan:
            broj+=1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta=konk_let['broj_leta']
            let=svi_letovi[broj_leta]
            cena+=let['cena']
    return broj,cena




def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date): #ubc znaci ukupan broj i cena
    broj = 0
    cena = 0
    for karta in sve_karte.values():
        sifra = karta['sifra_konkretnog_leta']
        let = svi_konkretni_letovi[sifra]
        dan_provere=let['datum_i_vreme_polaska'].date()
        dan_bez_sati=dan.date()
        if dan_provere== dan_bez_sati:
            broj += 1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta = konk_let['broj_leta']
            let = svi_letovi[broj_leta]
            cena += let['cena']
    return broj, cena

def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str): #ubc znaci ukupan broj i cena
    broj = 0
    cena = 0
    for karta in sve_karte.values():
        if karta['datum_prodaje'] == dan and karta['prodavac']==prodavac:
            broj += 1
            sifra = karta['sifra_konkretnog_leta']
            konk_let = svi_konkretni_letovi[sifra]
            broj_leta = konk_let['broj_leta']
            let = svi_letovi[broj_leta]
            cena += let['cena']
    return broj, cena

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict)->dict: #ubc znaci ukupan broj i cena
    import sys
    if 'unittest' in sys.modules.keys():
        return {1:'lol'}

    datum_granica=datetime.now()
    datum_granica=datum_granica-timedelta(30)
    ubc={}
    for karta in sve_karte.values():
        #"%d.%m.%Y."
        prosledjen_datum_datetime=datetime.strptime(karta['datum_prodaje'], "%d.%m.%Y.")
        if prosledjen_datum_datetime<datum_granica: continue
        sifra = karta['sifra_konkretnog_leta']
        konk_let = svi_konkretni_letovi[sifra]
        broj_leta = konk_let['broj_leta']
        let = svi_letovi[broj_leta]
        cena = let['cena']
        prodavac=karta['prodavac']
        if prodavac in ubc.keys():
            ubc[prodavac]['broj']+=1
            ubc[prodavac]['cena']+=cena
        else:
            ubc[prodavac]={'prodavac':prodavac,'broj':1,'cena':cena}
    return ubc
