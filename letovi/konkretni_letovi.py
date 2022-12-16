from common.konstante import PONEDELJAK,UTORAK,SREDA,CETVRTAK,PETAK,SUBOTA,NEDELJA
import json
from datetime import datetime, timedelta
import time
from model.model import vrati_sedista
from ast import literal_eval


def kreiraj_konkretan_let(svi_letovi, svi_konkretni_letovi, sifra:int , broj_leta, datum_i_vreme_polaska, datum_i_vreme_dolaska, zauzetost=[]):

    if zauzetost==[]:
        model_aviona=svi_letovi[broj_leta]["model"]
        zauzetost=vrati_sedista(model_aviona)


    konkretan_let = {
        "sifra": sifra,
        "broj_leta": broj_leta,
        "datum_i_vreme_polaska": datum_i_vreme_polaska,
        "datum_i_vreme_dolaska": datum_i_vreme_dolaska,
        "zauzetost": zauzetost,  # bilo koja vrsta kolekcije koja je adekvatna
    }
    svi_konkretni_letovi[sifra]=konkretan_let
    return svi_konkretni_letovi

def sacuvaj_konkretne_letove(putanja,separator,svi_konkretni_letovi):
    red_cuvanja=['sifra','broj_leta','datum_i_vreme_polaska','datum_i_vreme_dolaska','zauzetost']
    with open(putanja, 'w') as f:
        for let in svi_konkretni_letovi.values():
            nov_red=""
            for key in red_cuvanja:
                nov_red+= str(let[key]).replace(',','~')+separator
            f.write(nov_red)

def ucitaj_konkretne_letove(putanja,separator):
    svi_konk_let={}
    with open(putanja, 'r') as f:
        konkretni_letovi = f.readlines()

    for red in konkretni_letovi:
        if red=="": continue
        let={}
        red=red.split(separator)
        #red_cuvanja = ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska', 'zauzetost']
        let['sifra']=int(red[0])
        let['broj_leta']=red[1]
        let['datum_i_vreme_polaska']=datetime.strptime(red[2],"%Y-%m-%d %H:%M:%S")
        let['datum_i_vreme_dolaska'] = datetime.strptime(red[3], "%Y-%m-%d %H:%M:%S")
        red[4] = red[4].replace('~', ',')
        #red[4] = red[4].replace("\'", "")
        red[4] = red[4].replace(" ", "")
        #let['zauzetost'] = red[4].strip('][').replace(" ", "").split(',')
        let['zauzetost']=literal_eval(red[4]) #krajnje nesigurno
        svi_konk_let[let["sifra"]]=let
    return svi_konk_let

if __name__=="__main__":
    pass