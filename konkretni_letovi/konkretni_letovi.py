from datetime import datetime,timedelta
import letovi.letovi
from ast import literal_eval

sledeca_sifra_konkretnog_leta =1
def sledeca_sifra_konkretnog_leta_set(svi_konkretni_letovi):
    ids=svi_konkretni_letovi.keys()
    ids=list(ids)
    ids.sort()
    if len(ids)>0: id=ids[-1]+1 #uzme se najveci i doda 1
    else: id=1 #ako nema uopste postavi se na jedan

    return id

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict):


    sletanje_sutra=let['sletanje_sutra']

    datum_trenutni=let['datum_pocetka_operativnosti']
    datum_kraja=let['datum_kraja_operativnosti']

    while datum_trenutni<datum_kraja:
        datum_trenutni+=timedelta(days=1) #Increment
        if not datum_trenutni.weekday() in let['dani']: continue #Ako tog dana nema let idi dalje
        konkretan_let = {}
        konkretan_let['broj_leta'] = let['broj_leta']


        #Postavljanje sifre leta
        sledeca_sifra_konkretnog_leta=sledeca_sifra_konkretnog_leta_set(svi_konkretni_letovi)
        konkretan_let['sifra']=sledeca_sifra_konkretnog_leta

        #Datum je tog dana koji   se proverava
        datum_i_vreme_polaska=datum_trenutni
        datum_i_vreme_dolaska=datum_trenutni
        if sletanje_sutra: datum_i_vreme_dolaska+=timedelta(days=1) #Ako slece sutra dodaj dan

        vreme_poletanja=let['vreme_poletanja']
        vreme_poletanja=vreme_poletanja.split(':')
        sati,minuti=vreme_poletanja #Uzimanje sati i minuta
        datum_i_vreme_polaska=datum_i_vreme_polaska.replace(hour=int(sati),minute=int(minuti))
        konkretan_let['datum_i_vreme_polaska']=datum_i_vreme_polaska

        vreme_sletanja = let['vreme_sletanja']
        vreme_sletanja=vreme_sletanja.split(':')
        sati, minuti = vreme_sletanja#Uzimanje sati i minuta
        datum_i_vreme_dolaska=datum_i_vreme_dolaska.replace(hour=int(sati), minute=int(minuti))
        konkretan_let['datum_i_vreme_dolaska']=datum_i_vreme_dolaska

        svi_konkretni_letovi[sledeca_sifra_konkretnog_leta]=konkretan_let

    return svi_konkretni_letovi




"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    red_cuvanja = ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska','zauzetost','zauazetost']
    with open(putanja, 'w') as f:
        for let in svi_konkretni_letovi.values():
            nov_red = ""
            for key in red_cuvanja:
                #Cuva se u datom redosledu
                if key in let.keys():
                    nov_red += str(let[key]).replace(',','~')
                    nov_red+=separator
            nov_red=nov_red[:-1] #oduzima  se bespotrebni separator
            nov_red+='\n'
            f.write(nov_red)


"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    svi_konk_let = {}
    with open(putanja, 'r') as f:
        konkretni_letovi = f.readlines()

    for red in konkretni_letovi:
        if red == "": continue #Ako je let prazan preskoci
        red=red.rstrip('\n')
        let = {}
        red = red.split(separator)
        # red_cuvanja = ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska']
        let['sifra'] = int(red[0])
        let['broj_leta'] = red[1]
        let['datum_i_vreme_polaska'] = datetime.strptime(red[2], "%Y-%m-%d %H:%M:%S")
        let['datum_i_vreme_dolaska'] = datetime.strptime(red[3], "%Y-%m-%d %H:%M:%S")
        if len(red)>4:
            lista=red[4].replace('~',',')
            lista=literal_eval(lista)
            let['zauzetost']=lista
        svi_konk_let[let["sifra"]] = let
    return svi_konk_let

if __name__=='__main__':
    pass