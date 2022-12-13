import copy
import os
import random
import unittest

from common import konstante
from letovi import letovi
from test.test_utils import rand_str, rand_valid_user, rand_time_str, rand_date_str, rand_seat_positions


class LetoviTest(unittest.TestCase):
    def setUp(self):
        self.modeli_aviona = {
            123: {
                "id": 123,
                "naziv": rand_str(10),
                "broj_redova": random.randint(20, 50),
                "pozicija_sedista": rand_seat_positions()
            },
            124: {
                "id": 124,
                "naziv": rand_str(10),
                "broj_redova": random.randint(20, 50),
                "pozicija_sedista": rand_seat_positions()
            }
        }

        broj_leta = rand_str(4)

        self.konkretan_let = {
            "sifra": 1234,
            "broj_leta": broj_leta,
            "datum_polaska": rand_date_str(),
            "datum_dolaska": rand_date_str()
        }
        dani = list({random.randint(0, 6): True for n in range(random.randint(1, 7))}.keys())
        dani.sort()
        self.pun_let = {
            "broj_leta": broj_leta,
            "sifra_polazisnog_aerodroma": rand_str(3), #pitanje, da li je u redu da stavim ovako nazive, ili nekako drugacije?
            "sifra_odredisnog_aerodorma": rand_str(3),
            "vreme_poletanja": rand_time_str(),#pitanje, da li je u redu da stavim ovako vreme, ili nekako drugacije?
            "vreme_sletanja": rand_time_str(),
            "sletanje_sutra": False,
            "prevoznik": rand_str(10),
            "dani": dani,
            "model": self.modeli_aviona[123],
            "cena": 100 + random.random() * 200
        }
        self.pun_korisnik = rand_valid_user()

        self.putanja = "test_letovi.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_validan_let(self):
        svi_letovi = letovi.kreiranje_letova(
            {},
            self.pun_let["broj_leta"],
            self.pun_let["sifra_polazisnog_aerodroma"],
            self.pun_let["sifra_odredisnog_aerodorma"],
            self.pun_let["vreme_poletanja"],
            self.pun_let["vreme_sletanja"],
            self.pun_let["sletanje_sutra"],
            self.pun_let["prevoznik"],
            self.pun_let["dani"],
            self.pun_let["model"],
            self.pun_let["cena"],
        )
        self.assertIsNotNone(svi_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], svi_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            svi_letovi[self.pun_let["broj_leta"]],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_kreiraj_prazni(self):
        for key in self.pun_let:
            let = copy.deepcopy(self.pun_let)
            let[key] = None

        rezultat = letovi.kreiranje_letova(
            {},
            let["broj_leta"],
            let["sifra_polazisnog_aerodroma"],
            let["sifra_odredisnog_aerodorma"],
            let["vreme_poletanja"],
            let["vreme_sletanja"],
            let["sletanje_sutra"],
            let["prevoznik"],
            let["dani"],
            let["model"],
            let["cena"],)
        print(rezultat)
        self.assertTrue(type(rezultat) is str, msg=f"Provera za nedostajucu vrednost: {key}")
        self.assertTrue(len(rezultat)>0, msg=f"Provera za nedostajucu vrednost: {key}")

    def test_kreiraj_prazni_let(self):
        for key in self.pun_let:
            let = copy.deepcopy(self.pun_let)
            let[key] = ""
        let["model"] = 0
        let["cena"] = 0
        rezultat = letovi.kreiranje_letova(
            {},
            let["broj_leta"],
            let["sifra_polazisnog_aerodroma"],
            let["sifra_odredisnog_aerodorma"],
            let["vreme_poletanja"],
            let["vreme_sletanja"],
            let["sletanje_sutra"],
            let["prevoznik"],
            let["dani"],
            let["model"],
            let["cena"],)
        self.assertTrue(type(rezultat) is str, msg=f"Provera za nedostajucu vrednost: {key}")
        self.assertTrue(len(rezultat)>0, msg=f"Provera za nedostajucu vrednost: {key}")

    def test_kreiraj_nevalidan_let_broj_leta(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: broj leta"):
            rezultat = letovi.kreiranje_letova(
                {},
                "aaaaaa",
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"])

    def test_kreiraj_nevalidan_let_vreme_polaska(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme polaska"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                "12345",
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"])

    def test_kreiraj_nevalidan_let_vreme_dolaska(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme dolaska"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                "12345",
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                self.pun_let["cena"])


    def test_kreiraj_nevalidan_let_dani(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: losi dani"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                None, #pitanje ili da posaljem [] ?
                self.pun_let["model"],
                self.pun_let["cena"])

    def test_kreiraj_nevalidan_let_cena(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: cena"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"],
                -345)

    def test_kreiraj_nevalidan_let_model(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: model"):
            rezultat = letovi.kreiranje_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodroma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                None,
                self.pun_let["cena"])

    #--------------------------------------------------------------
    def test_uspesna_pretraga_letova_polaziste(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]:self.konkretan_let},
            self.pun_let["sifra_polazisnog_aerodroma"]
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_odrediste(self): # da li ovde da dodam vise letova pa nekako drugacije da vratim??? razmisli
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            self.pun_let["sifra_odredisnog_aerodorma"]
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_datum_polaska(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            self.konkretan_let["datum_polaska"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_datum_dolaska(self):
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            "",
            self.konkretan_let["datum_dolaska"]
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_vreme_poletanja(self): # da li ovde da dodam vise letova pa nekako drugacije da vratim??? razmisli
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            "",
            "",
            self.pun_let["vreme_poletanja"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_vreme_sletanja(self): # da li ovde da dodam vise letova pa nekako drugacije da vratim??? razmisli
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            "",
            "",
            "",
            self.pun_let["vreme_sletanja"], # da li ovo ide bas po sifri ili po imenu pa tako nekako
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_prevoznik(self): # da li ovde da dodam vise letova pa nekako drugacije da vratim??? razmisli
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            "",
            "",
            "",
            "",
            self.pun_let["prevoznik"],
           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_uspesna_pretraga_letova_visekriterijumska(self): # da li ovde da dodam vise letova pa nekako drugacije da vratim??? razmisli
        trazeni_letovi = letovi.pretraga_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            self.pun_let["sifra_polazisnog_aerodroma"], # da li ovo ide bas po sifri ili po imenu pa tako nekako
            self.pun_let["sifra_odredisnog_aerodorma"],
            "",
            "",
            self.pun_let["vreme_poletanja"],
            self.pun_let["sifra_vreme_sletanja"],
            self.pun_let["prevoznik"],

           )
        self.assertIsNotNone(trazeni_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], trazeni_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            self.pun_let,
            trazeni_letovi[0],
            msg="Vrednosti od leta nisu dobre"
        )


    def test_neuspesna_pretraga(self):
        with self.assertRaises(Exception, msg=f"Neuspesno trazenje leta"):
            trazeni_letovi = letovi.pretraga_letova(
                {self.pun_let["broj_leta"]: self.pun_let},
                {self.konkretan_let["sifra"]: self.konkretan_let},
                "LKI",  # da li ovo ide bas po sifri ili po imenu pa tako nekako
                "NJH",
                "",
                "",
                "aaaaa",
                self.pun_let["sifra_vreme_sletanja"],
                self.pun_let["prevoznik"])

    #--------------------------------------------------------------
    def test_uspesno_trazenje_10_najjeftinijih_letova(self):
        pass

    def test_neuspesno_trazenje_10_najjeftinijih_letova(self):
        pass

    #--------------------------------------------------------------
    def test_uspesna_izmena_letova(self):
        nov_let={
            "broj_leta": "aa33",
            "sifra_polazisnog_aerodroma": "LON",
            "sifra_odredisnog_aerodorma": "SAO",
            "vreme_poletanja": "10:45",
            "vreme_sletanja": "7:30",
            "sletanje_sutra": True,
            "prevoznik": "prevoznik1",
            "dani": [konstante.SUBOTA, konstante.PONEDELJAK],
            "model": self.modeli_aviona[124],
            "cena": 200
        }
        svi_letovi = letovi.izmena_letova(
            {self.pun_let["broj_leta"]: self.pun_let},
            self.pun_let["broj_leta"], #ostavicu da ne menja br leta pa ako zatreba dodacemo
            nov_let["sifra_polazisnog_aerodroma"],
            nov_let["sifra_odredisnog_aerodorma"],
            nov_let["vreme_poletanja"],
            nov_let["vreme_sletanja"],
            nov_let["sletanje_sutra"],
            nov_let["prevoznik"],
            nov_let["dani"],
            nov_let["model"],
            nov_let["cena"],
        )
        self.assertIsNotNone(svi_letovi, msg="Nije vraćena kolekcija letova")
        self.assertIn(self.pun_let["broj_leta"], svi_letovi, msg="Let nije u kolekciji")
        self.assertDictEqual(
            nov_let,
            svi_letovi[nov_let["broj_leta"]],
            msg="Vrednosti od leta nisu dobre"
        )

    def test_neuspesna_izmena_letova(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: polaziste"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                "3333333",
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_nepostojeci_let(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: nepostojeci let"):
            rezultat = letovi.izmena_letova(
                {},
                "789989",
                "3333333",
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_polaziste(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: polaziste"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                "3333333",
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_odrediste(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: odrediste"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                "3333333",
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_vreme_poletanja(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme leta"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                "3333333",
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_vreme_sletanja(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: vreme sletanja"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                "5555555",
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_sletanje_sutra(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: sletanje sutra"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                 self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                None,
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_prevoznik(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost:prevoznik"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                None, #ili nesto drugo
                self.pun_let["dani"],
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_dani(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: dani"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                None,
                self.pun_let["model"])

    def test_neuspesna_izmena_letova_model(self):
        with self.assertRaises(Exception, msg=f"Provera za nevalidnu vrednost: model"):
            rezultat = letovi.izmena_letova(
                {},
                self.pun_let["broj_leta"],
                self.pun_let["sifra_polazisnog_aerodorma"],
                self.pun_let["sifra_odredisnog_aerodorma"],
                self.pun_let["vreme_poletanja"],
                self.pun_let["vreme_sletanja"],
                self.pun_let["sletanje_sutra"],
                self.pun_let["prevoznik"],
                self.pun_let["dani"],
                None)

    def testiraj_letovi_fajl(self):
        let2 = copy.deepcopy(self.pun_let)
        let2["broj_leta"]="aa34"
        let2["sifra_polazisnog_aerodroma"]="TYO"
        let3 = copy.deepcopy(self.pun_let)
        let3["broj_leta"] = "aa35"
        let3["sifra_odredisnog_aerodorma"] = "TYO"
        referentni_letovi = {
            self.pun_let["broj_leta"]: self.pun_let,
            let2["broj_leta"]: let2,
            let3["broj_leta"]: let3
        }
        letovi.sacuvaj_letove(self.putanja, "|", referentni_letovi)

        ucitani_letovi = letovi.ucitaj_letove_iz_fajla(self.putanja, "|")
        self.assertIsNotNone(ucitani_letovi, msg="Nisu učitani letovi iz fajla")
        self.assertEqual(len(referentni_letovi), len(ucitani_letovi), msg="Dužine učitanih letova nisu jednake")
        for k in ucitani_letovi:
            ucitani_let = ucitani_letovi[k]
            self.assertDictEqual(referentni_letovi[k], ucitani_let, msg="Učitani letovi se ne poklapaju")


if __name__ == '__main__':
    unittest.main()
