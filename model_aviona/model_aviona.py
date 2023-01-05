
"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicija_sedista: list = []
) -> dict:
    if naziv=="" or naziv is None: raise Exception("Naziv je prazan")
    if broj_redova=='' or broj_redova is None: raise Exception("Broj redova prazan")
    if pozicija_sedista==[] or pozicija_sedista is None: raise Exception("Pozicija sedista prazna")

    sledeci_id=sledeci_id_set(svi_modeli_aviona)
    model = {"id": sledeci_id, "naziv": naziv, "broj_redova": broj_redova, "pozicije_sedista": pozicija_sedista}
    svi_modeli_aviona[sledeci_id] = model
    sacuvaj_modele_aviona('./fajlovi/modeli.csv',',',svi_modeli_aviona)
    return svi_modeli_aviona

sledeci_id=0

def sledeci_id_set(svi_modeli_aviona):
    ids = svi_modeli_aviona.keys()
    ids = list(ids)
    ids.sort()
    if len(ids) > 0:
        id = ids[-1] + 1  # uzme se najveci i doda 1
    else:
        id = 0  # ako nema uopste postavi se na jedan

    return id

def vrati_sedista(model: dict) -> list:
    red=['X']*len(model["pozicije_sedista"])
    redovi=[red]*model['broj_redova']
    return redovi

"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_modeli_aviona: dict):
    red_cuvanja=['id','naziv','broj_redova','pozicija_sedista']
    with open(putanja,'w') as f:
        for model_aviona in svi_modeli_aviona.values():
            red=''
            red+=str(model_aviona['id'])+separator
            red+=model_aviona['naziv']+separator
            red += str(model_aviona['broj_redova'])+separator
            red += ''.join(model_aviona['pozicije_sedista'])+'\n'
            f.write(red)

"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    svi_modeli = {}
    with open(putanja, 'r') as f:
        redovi = f.readlines()

    for red in redovi:
        red = red.rstrip('\n')
        red = red.split(separator)
        model = {}
        # Realno bi moglo sa enumarate al me mrzi
        model['id']=int(red[0])
        model['naziv'] = red[1]
        model['broj_redova'] = int(red[2])
        model['pozicije_sedista'] = list(red[3])
        svi_modeli[model['id']] = model
    return svi_modeli
