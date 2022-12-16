from common.konstante import PONEDELJAK,UTORAK,SREDA,CETVRTAK,PETAK,SUBOTA,NEDELJA
import json
from datetime import datetime, timedelta
import time

def kreiraj_konkretan_let(svi_konkretni_letovi,sifra, broj_leta, datum_i_vreme_polaska, datum_i_vreme_dolaska, zauzetost=):
    konkretan_let = {
        "sifra": sifra,
        "broj_leta": broj_leta,
        "datum_i_vreme_polaska": datum_i_vreme_polaska,
        "datum_i_vreme_dolaska": datum_i_vreme_dolaska,
        "zauzetost": zauzetost,  # bilo koja vrsta kolekcije koja je adekvatna
    }
    svi_konkretni_letovi[sifra]=konkretan_let
    return svi_konkretni_letovi

def sacuvaj_konkretne_letove(putanja,svi_konkretni_letovi):
    red_cuvanja=['sifra','broj_leta','datum_i_vreme_polaska','datum_i_vreme_dolaska','zauzetost']
    with open(putanja, 'w') as f:
        for value in svi_konkretni_letovi.values():
            nov_red=str(value)+'\n'
            f.write(nov_red)

def ucitaj_konkretne_letove(putanja):
    svi_konk_let={}
    with open(putanja, 'r') as f:
        letovi = f.readlines()

    for let in letovi:
        if let=="": continue
        let=let.rstrip('\n')
        let=let.replace("\'","\"")
        print(let)
        let=json.loads(let)
        svi_konk_let[let["id"]]=let
    return svi_konk_let

if __name__=="__main__":
    svi_let=kreiraj_konkretan_let({},"1234","JU50",datetime(2022,12,16,15,0,0),datetime(2022,12,16,16,0,0),[])
    sacuvaj_konkretne_letove("./konk_let.csv",svi_let)
    svi_let=ucitaj_konkretne_letove("./konk_let.csv")
    #print(svi_let)
