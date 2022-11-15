import os
import unittest
import copy
import random

from korisnici import korisnici
from test.test_utils import rand_str, rand_valid_user

class KorisnikTest(unittest.TestCase):
    def setUp(self):
        self.pun_korisnik = rand_valid_user()
        self.putanja = "test_korisnici.csv"
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def tearDown(self):
        if os.path.isfile(self.putanja):
            os.remove(self.putanja)

    def test_kreiraj_validnog_korisnika(self):
        svi_korisnici = korisnici.kreiraj_korisnika(
            {},
            False,  # azuriraj
            self.pun_korisnik["uloga"],
            self.pun_korisnik["korisnicko_ime"],
            self.pun_korisnik["lozinka"],
            self.pun_korisnik["ime"],
            self.pun_korisnik["prezime"],
            self.pun_korisnik["email"],
            self.pun_korisnik["pasos"],
            self.pun_korisnik["drzavljanstvo"],
            self.pun_korisnik["telefon"],
            self.pun_korisnik["pol"])
        self.assertDictEqual(self.pun_korisnik, svi_korisnici[self.pun_korisnik["korisnicko_ime"]])

    def test_azuriraj_validnog_korisnika(self):
        korisnik = {key: rand_str(10) for key in self.pun_korisnik}
        korisnik["korisnicko_ime"] = self.pun_korisnik["korisnicko_ime"]
        korisnik["uloga"] = self.pun_korisnik["uloga"]
        korisnik["pasos"] = random.randint(100000001, 999999999)
        korisnik["telefon"] = random.randint(100000001, 999999999)
        korisnik["email"] += "@email.com"
        svi_korisnici = {
            self.pun_korisnik["korisnicko_ime"]: self.pun_korisnik
        }

        svi_korisnici = korisnici.kreiraj_korisnika(
            svi_korisnici,
            True, # azuriraj
            korisnik["uloga"],
            korisnik["korisnicko_ime"],
            korisnik["lozinka"],
            korisnik["ime"],
            korisnik["prezime"],
            korisnik["email"],
            korisnik["pasos"],
            korisnik["drzavljanstvo"],
            korisnik["telefon"],
            korisnik["pol"])
        self.assertDictEqual(korisnik, svi_korisnici[self.pun_korisnik["korisnicko_ime"]])

    def test_kreiraj_prazni(self):
        # Prodji kroz sve kljuceve, postavi jedan na None, pa pozovi funkciju
        for key in self.pun_korisnik:
            korisnik = copy.deepcopy(self.pun_korisnik)
            korisnik[key] = None
            with self.assertRaises(Exception, msg=f"Provera za nedostajucu vrednost: {key}"):
                korisnici.kreiraj_korisnika(
                    {},
                    False,  # azuriraj
                    korisnik["uloga"],
                    korisnik["korisnicko_ime"],
                    korisnik["lozinka"],
                    korisnik["ime"],
                    korisnik["prezime"],
                    korisnik["email"],
                    korisnik["pasos"],
                    korisnik["drzavljanstvo"],
                    korisnik["telefon"],
                    korisnik["pol"])

    def test_kreiraj_postojece_korisnicko_ime(self):
        with self.assertRaises(Exception, msg="Postojece korisnicko ime"):
            svi_korisnici = {
                self.pun_korisnik["korisnicko_ime"]: self.pun_korisnik
            }
            korisnici.kreiraj_korisnika(
                svi_korisnici,
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                self.pun_korisnik["pasos"],
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

    def test_azuriraj_nepostojece_korisnicko_ime(self):
        with self.assertRaises(Exception, msg="Postojece korisnicko ime"):
            svi_korisnici = {
                self.pun_korisnik["korisnicko_ime"]: self.pun_korisnik
            }
            korisnici.kreiraj_korisnika(
                {},
                True,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                self.pun_korisnik["pasos"],
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

    def test_email(self):
        with self.assertRaises(Exception, msg="Email provera bez @"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                "email_bez_at",
                self.pun_korisnik["pasos"],
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

        with self.assertRaises(Exception, msg="Email provera sa @ ali sa više poddomena"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                "email@email.vise.poddomena",
                self.pun_korisnik["pasos"],
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

    def test_pasos(self):
        with self.assertRaises(Exception, msg="Pasoš nebrojevni string"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                "abcdefghi",
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

        with self.assertRaises(Exception, msg="Pasoš manje od 9 cifara"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                123,
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

        with self.assertRaises(Exception, msg="Pasoš više od 9 cifara"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                111111111111,
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])

    def test_broj_telefona(self):
        with self.assertRaises(Exception, msg="Broj telefona nebrojevni string"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                self.pun_korisnik["uloga"],
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                self.pun_korisnik["pasos"],
                self.pun_korisnik["drzavljanstvo"],
                "abcdefghi",
                self.pun_korisnik["pol"])

    def test_uloga(self):
        with self.assertRaises(Exception, msg="Broj telefona nebrojevni string"):
            korisnici.kreiraj_korisnika(
                {},
                False,  # azuriraj
                "nepoznata_uloga",
                self.pun_korisnik["korisnicko_ime"],
                self.pun_korisnik["lozinka"],
                self.pun_korisnik["ime"],
                self.pun_korisnik["prezime"],
                self.pun_korisnik["email"],
                self.pun_korisnik["pasos"],
                self.pun_korisnik["drzavljanstvo"],
                self.pun_korisnik["telefon"],
                self.pun_korisnik["pol"])


    def testiraj_korisnici_fajl(self):
        referentni_korisnici = {}
        for i in range(10):
            korisnik = {key: rand_str(10) for key in self.pun_korisnik}
            korisnik["uloga"] = self.pun_korisnik["uloga"]
            korisnik["pasos"] = random.randint(100000001, 999999999)
            korisnik["telefon"] = random.randint(100000001, 999999999)
            korisnik["email"] += "@email.com"
            referentni_korisnici[korisnik["korisnicko_ime"]] = korisnik

        korisnici.sacuvaj_korisnike(self.putanja, "|", referentni_korisnici)

        ucitani_korisnici = korisnici.ucitaj_korisnike_iz_fajla(self.putanja, "|")
        self.assertEqual(len(referentni_korisnici), len(ucitani_korisnici))
        for korisnicko_ime in ucitani_korisnici:
            ucitani_korisnik = ucitani_korisnici[korisnicko_ime]
            self.assertDictEqual(referentni_korisnici[korisnicko_ime], ucitani_korisnik)

    def testiraj_login(self):
        korisnicko_ime = self.pun_korisnik["korisnicko_ime"]
        lozinka = self.pun_korisnik["lozinka"]
        svi_korisnici = {
            korisnicko_ime: self.pun_korisnik
        }

        with self.assertRaises(Exception, msg="Login nepostojeći"):
            korisnici.login(svi_korisnici, "mika", "mikic")

        with self.assertRaises(Exception, msg="Login pogrešna lozinka"):
            korisnici.login(svi_korisnici, korisnicko_ime, "321")
        pronadjeni_korisnik = korisnici.login(svi_korisnici, korisnicko_ime, lozinka)
        self.assertDictEqual(self.pun_korisnik, pronadjeni_korisnik, msg="Uspešan login")


if __name__ == '__main__':
    unittest.main()
