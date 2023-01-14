

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    aerodrom={
        'skracenica':skracenica,
        'pun_naziv': pun_naziv,
        'grad': grad,
        'drzava': drzava
    }
    for key,val in aerodrom.items():
        if val=='': raise Exception(f'{key.capitalize()} je prazan')

    svi_aerodromi[skracenica]=aerodrom
    return svi_aerodromi

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    red_cuvanja=['skracenica', 'pun_naziv', 'grad', 'drzava']

    with open(putanja,'w') as f:
        for aerodrom in svi_aerodromi.values():
            red=''
            for key in red_cuvanja:
                red+=aerodrom[key]+separator
            red=red[:-1]+'\n'
            f.write(red)


"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    red_cuvanja=['skracenica', 'pun_naziv', 'grad', 'drzava']
    svi_aerodromi={}
    with open(putanja,'r') as f:
        redovi=f.readlines()

    for red in redovi:
        red=red.rstrip('\n')
        red=red.split(separator)
        aerodrom={}
        #Realno bi moglo sa enumarate al me mrzi
        aerodrom['skracenica']=red[0]
        aerodrom['pun_naziv'] = red[1]
        aerodrom['grad'] = red[2]
        aerodrom['drzava'] = red[3]
        svi_aerodromi[aerodrom['skracenica']]=aerodrom

    return svi_aerodromi

if __name__=='__main__':
    svi_aerodromi=ucitaj_aerodrom('./aerodrom.csv',',')
    svi_aerodromi=kreiranje_aerodroma(svi_aerodromi,
                                      'TKY',
                                      'Tokyo Airport',
                                      'Tokijo',
                                      'Japan')
    sacuvaj_aerodrome('./aerodrom.csv',',',svi_aerodromi)