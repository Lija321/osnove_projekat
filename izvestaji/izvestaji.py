from datetime import datetime, date
from functools import reduce

def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: datetime)->list:
    pass

def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date):
    pass

def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str):
    pass

def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    pass



def izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict, dan: date): #ubc znaci ukupan broj i cena
    pass

def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, konkretni_letovi: dict, svi_letovi: dict, dan: date, prodavac: str): #ubc znaci ukupan broj i cena
    pass

def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte: dict, svi_konkretni_letovi: dict, svi_letovi: dict)->dict: #ubc znaci ukupan broj i cena
    pass


