import sqlite3
from osoba import Osoba

# konstanta pro název souboru
DB_NAZEV_SLOZKY = "databaze.db"


class EvidencePojisteniDB:
    """
    Třída pracující s databázi
    Vytvoření tabulky, vytvoření záznamů v tabulce, zobrazení údajů v tabulce, vyhledávání v tabulce, smazání údajů v tabulce
    """

    def __init__(self):
        """
        Inicializace instance třídy a připojení k databázi
        """
        self.pripojeni = sqlite3.connect(DB_NAZEV_SLOZKY)  # připojení k databázi
        self.kurzor = self.pripojeni.cursor()

    def vytvoreni_databazove_tabulky(self):
        """
        Vytvoření tabulky v databázi pro ukládání informací o pojištěných osobách
        """
        self.kurzor.execute(
            "CREATE TABLE IF NOT EXISTS uzivatele(jmeno, prijmeni, vek, telefon)"
        )

    def pridej_pojisteneho_do_evidence(self, novy_pojisteny):
        """
        Přidání nového pojištěného do databáze
        """
        self.kurzor.execute(
            "INSERT INTO uzivatele VALUES (?, ?, ?, ?)",
            (
                novy_pojisteny.jmeno,
                novy_pojisteny.prijmeni,
                novy_pojisteny.vek,
                novy_pojisteny.telefon,
            ),
        )
        self.pripojeni.commit()  # Potvrzení provedených změn v databázi

    def vrat_vsechny_pojistene(self):
        """
        Získání všech pojištěných osob z databáze
        """
        self.kurzor.execute("SELECT * FROM uzivatele")
        vsechny_osoby = self.kurzor.fetchall()
        seznam_osob = []

        # Převod záznamů z databáze na objekty třídy Osoba
        for osoba in vsechny_osoby:
            seznam_osob.append(Osoba(*osoba))

        return seznam_osob

    def vyhledej_pojistene(self, jmeno, prijmeni):
        """
        Vyhledávání pojištěných osob v databázi podle jména a příjmení
        """
        self.kurzor.execute(
            "SELECT * FROM uzivatele WHERE jmeno LIKE ? AND prijmeni LIKE ?",
            ("%" + jmeno + "%", "%" + prijmeni + "%"),
        )
        hledane_osoby = self.kurzor.fetchall()
        nalezene_osoby = []

        # Převod záznamů z databáze na objekty třídy Osoba
        for jmeno in hledane_osoby:
            nalezene_osoby.append(Osoba(*jmeno))

        return nalezene_osoby

    def vymaz_vsechny_pojistene(self):
        """
        Smazání všech záznamů o pojištěných osobách z databáze
        """
        self.kurzor.execute("DELETE FROM uzivatele")
        # Potvrzení provedených změn v databázi
        self.pripojeni.commit()
