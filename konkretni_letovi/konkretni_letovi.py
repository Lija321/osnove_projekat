from datetime import datetime, timedelta

sledeca_sifra_konkretnog_leta =1
def sledeca_sifra_konkretnog_leta_set(svi_konkretni_letovi):
    ids=svi_konkretni_letovi.keys()
    ids=list(ids)
    ids.sort()
    if len(ids)>0: id=ids[-1]+1
    else: id=1

    return id
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict):

    konkretan_let = {}
    konkretan_let['broj_leta'] = let['broj_leta']
    sletanje_sutra=let['sletanje_sutra']
    datum_trenutni=let['datum_pocetka_operativnosti'] #zbog nacina na koji raste while
    datum_kraja=let['datum_kraja_operativnosti']
    while datum_trenutni<datum_kraja:
        datum_trenutni+=timedelta(days=1)
        if not datum_trenutni.weekday() in let['dani']: continue

        sledeca_sifra_konkretnog_leta=sledeca_sifra_konkretnog_leta_set(svi_konkretni_letovi)
        konkretan_let['sifra']=sledeca_sifra_konkretnog_leta
        datum_i_vreme_polaska=datum_trenutni
        datum_i_vreme_dolaska=datum_trenutni
        if sletanje_sutra: datum_i_vreme_dolaska+=timedelta(days=1)

        vreme_poletanja=let['vreme_poletanja']
        vreme_poletanja=vreme_poletanja.split(':')
        sati,minuti=vreme_poletanja
        datum_i_vreme_polaska=datum_i_vreme_polaska.replace(hour=int(sati),minute=int(minuti))
        konkretan_let['datum_i_vreme_polaska']=datum_i_vreme_polaska

        vreme_sletanja = let['vreme_sletanja']
        vreme_sletanja=vreme_sletanja.split(':')
        sati, minuti = vreme_sletanja
        datum_i_vreme_dolaska=datum_i_vreme_dolaska.replace(hour=int(sati), minute=int(minuti))
        konkretan_let['datum_i_vreme_dolaska']=datum_i_vreme_dolaska

        svi_konkretni_letovi[sledeca_sifra_konkretnog_leta]=konkretan_let


    return svi_konkretni_letovi


    sledeca_sifra_konkretnog_leta=sledeca_sifra_konkretnog_leta_set(svi_konkretni_letovi)


def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    red_cuvanja = ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska']
    with open(putanja, 'w') as f:
        for let in svi_konkretni_letovi.values():
            nov_red = ""
            for key in red_cuvanja:
                nov_red += str(let[key]).replace(',', '~') + separator
            nov_red+='\n'
            f.write(nov_red)

def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    svi_konk_let = {}
    with open(putanja, 'r') as f:
        konkretni_letovi = f.readlines()

    for red in konkretni_letovi:
        if red == "": continue
        let = {}
        red = red.split(separator)
        # red_cuvanja = ['sifra', 'broj_leta', 'datum_i_vreme_polaska', 'datum_i_vreme_dolaska']
        let['sifra'] = int(red[0])
        let['broj_leta'] = red[1]
        let['datum_i_vreme_polaska'] = datetime.strptime(red[2], "%Y-%m-%d %H:%M:%S")
        let['datum_i_vreme_dolaska'] = datetime.strptime(red[3], "%Y-%m-%d %H:%M:%S")
        #red[4] = red[4].replace('~', ',')
        # red[4] = red[4].replace("\'", "")
        #red[4] = red[4].replace(" ", "")
        # let['zauzetost'] = red[4].strip('][').replace(" ", "").split(',')
        #let['zauzetost'] = literal_eval(red[4])  # krajnje nesigurno
        svi_konk_let[let["sifra"]] = let
    return svi_konk_let

if __name__=='__main__':
    pass