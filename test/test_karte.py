import os
import unittest
import copy
import random

from common import konstante
from karte import karte
from test.test_utils import rand_str, rand_valid_user, rand_time_str, rand_date_str, rand_seat_positions
import random
import string

class KarteTest(unittest.TestCase):
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

        pozicije_sedista = self.modeli_aviona[123]["pozicija_sedista"]
        odabrano_sediste_red = random.randint(1, self.modeli_aviona[123]["broj_redova"])
        odabrano_sediste_pozicija = pozicije_sedista[random.randint(len(pozicije_sedista))]

        self.puna_karta = {
            "broj_karte": 1,
            "sifra_leta": 1234, #sifra konkretnog leta
             "sifra_konkretnog_leta": 1234,
            "kupac": rand_str(10), # k ime od kupca
            "prodavac": rand_str(10),
            "sifra_sedista": f"{odabrano_sediste_pozicija}{odabrano_sediste_red}",
            "datum_prodaje": rand_date_str(end=self.konkretan_let['datum_polaska']),
            "obrisana": False
        }

        self.putanja = "test_karte.csv"

        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)


    def test_izmena_karte(self):
        sve_karte = karte.izmena_karte(
            {self.puna_karta["broj_karte"]: self.puna_karta},
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            self.puna_karta["sifra_konkretnog_leta"],
            self.puna_karta["broj_karte"],
            self.konkretan_let["sifra"],
            "23.10.2023.",
            "a5"
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            self.puna_karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_izmena_karte_pogresan_let(self):
        with self.assertRaises(Exception, msg=f"Provera za nedostajucu vrednost: let"):
            sve_karte = karte.izmena_karte(
                {self.puna_karta["broj_karte"]: self.puna_karta},
                {self.pun_let["broj_leta"]: self.pun_let},
                {self.konkretan_let["sifra"]: self.konkretan_let},
                self.puna_karta["sifra_konkretnog_leta"],
                self.puna_karta["broj_karte"],
                "67868",
                "13.5.2024.",
                "A3"
            )

    def test_izmena_karte_pogresan_datum(self):
        with self.assertRaises(Exception, msg=f"Provera za datum koji je prosao"):
            sve_karte = karte.izmena_karte(
                {self.puna_karta["broj_karte"]: self.puna_karta},
                {self.pun_let["broj_leta"]: self.pun_let},
                {self.konkretan_let["sifra"]: self.konkretan_let},
                self.puna_karta["sifra_konkretnog_leta"],
                self.puna_karta["broj_karte"],
                self.puna_karta["sifra_leta"],
                "13.5.2020.",
                "a5"
            )


    def test_izmena_karte_pogresno_sediste(self):
        with self.assertRaises(Exception, msg=f"Provera za sediste koje ne postoji"):
            sve_karte = karte.izmena_karte(
                {self.puna_karta["broj_karte"]: self.puna_karta},
                {self.pun_let["broj_leta"]: self.pun_let},
                {self.konkretan_let["sifra"]: self.konkretan_let},
                self.puna_karta["sifra_konkretnog_leta"],
                self.puna_karta["broj_karte"],
                self.konkretan_let["sifra"],
                "12.12.2024.",
                ''.join(random.sample(string.ascii_lowercase, 4))
            )


    def test_brisanje_karte_prodavac(self):
        karta = copy.deepcopy(self.puna_karta)
        karta["obrisana"] = False
        sve_karte = karte.brisanje_karte_od_strane_prodavca(
            {self.puna_karta["broj_karte"]: self.puna_karta},
            self.puna_karta["broj_karte"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Korisnik nije u kolekciji")
        self.assertDictEqual(
            karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_neuspesno_brisanje_karte_prodavac(self):
        karta = copy.deepcopy(self.puna_karta)
        karta["obrisana"] = False
        with self.assertRaises(Exception, msg=f"Brisanje nepostojece karte"):
            karte.brisanje_karte_od_strane_prodavca(
                {self.puna_karta["broj_karte"]: self.puna_karta},
                "123"
            )

    #--------------------------------------------------------------
    def test_pretraga_prodatih_karata_polaziste(self):
        sve_karte = karte.pretraga_prodatih_karata(
            {self.puna_karta["broj_karte"]: self.puna_karta},
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            self.pun_let["sifra_polazisnog_aerodroma"],
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            self.puna_karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_pretraga_prodatih_karata_odrediste(self):
        sve_karte = karte.pretraga_prodatih_karata(
            {self.puna_karta["broj_karte"]:self.puna_karta},
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            self.pun_let["sifra_odredisnog_aerodroma"],
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            self.puna_karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_pretraga_prodatih_karata_datum_polaska(self):
        sve_karte = karte.pretraga_prodatih_karata(
            {self.puna_karta["broj_karte"]:self.puna_karta},
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]:self.konkretan_let},
            "",
            "",
            self.konkretan_let["datum_polaska"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            self.puna_karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_pretraga_prodatih_karata_datum_odlaska(self):
        sve_karte = karte.pretraga_prodatih_karata(
            {self.puna_karta["broj_karte"]:self.puna_karta},
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            "",
            self.puna_karta["datum_dolaska"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            self.puna_karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_pretraga_prodatih_karata_putnik_uspesno(self):
        sve_karte = karte.pretraga_prodatih_karata(
            {self.puna_karta["broj_karte"]: self.puna_karta},
            {self.pun_let["broj_leta"]: self.pun_let},
            {self.konkretan_let["sifra"]: self.konkretan_let},
            "",
            "",
            "",
            "",
            self.puna_karta["kupac"]
        )
        self.assertIsNotNone(sve_karte, msg="Nije vraćena kolekcija karata")
        self.assertIn(self.puna_karta["broj_karte"], sve_karte, msg="Karta nije u kolekciji")
        self.assertDictEqual(
            self.puna_karta,
            sve_karte[self.puna_karta["broj_karte"]],
            msg="Kartine vrednosti nisu dobre"
        )

    def test_pretraga_prodatih_karata_putnik_neuspesno(self):
        with self.assertRaises(Exception, msg=f"Prosledjene su lose vrednosti"):
            sve_karte = karte.pretraga_prodatih_karata(
                {self.puna_karta["broj_karte"]: self.puna_karta},
                {self.pun_let["broj_leta"]: self.pun_let},
                {self.konkretan_let["sifra"]: self.konkretan_let},
                None,
                None,
                None,
                None,
                None,
            )

    def testiraj_karte_fajl(self):
        karta2 = copy.deepcopy(self.puna_karta)
        karta2["broj_karte"]=2
        karta2["sifra_sedista"]="c2"
        karta3 = copy.deepcopy(self.puna_karta)
        karta3["broj_karte"] = 3
        karta3["sifra_sedista"] = "c3"
        referentne_karte = {
            self.puna_karta["broj_karte"]: self.puna_karta,
            karta2["broj_leta"]: karta2,
            karta3["broj_leta"]: karta3
        }
        karte.sacuvaj_karte(self.putanja, "|", referentne_karte)

        ucitane_karte = karte.ucitaj_karte_iz_fajla(self.putanja, "|")
        self.assertIsNotNone(ucitane_karte, msg="Nisu učitane karte iz fajla")
        self.assertEqual(len(referentne_karte), len(ucitane_karte), msg="Dužine učitanih karata nisu jednake")
        for k in ucitane_karte:
            ucitana_karta = ucitane_karte[k]
            self.assertDictEqual(referentne_karte[k], ucitana_karta, msg="Učitane karte se ne poklapaju")

if __name__ == '__main__':
    unittest.main()
