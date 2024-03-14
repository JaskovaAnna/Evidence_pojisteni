import re

from osoba import Osoba


class ValidatorVstupu:
    """
    Třída obsluhující kontrolu vstupů od uživatele
    """

    FORMAT_TELEFONU = re.compile(
        r"^(\+\d{1,4}\s?)?(\d{3}\s?\d{3}\s?\d{3})$"
    )  # Konstanta pro regulární výraz českého telefonního čísla

    def vstup_ziskej_jmeno(self, nazev):
        """
        Získává od uživatele jméno a příjmení pro vstup.

        :param nazev (str): Název, který bude zobrazen uživateli ("jméno" a "příjmení").
        """
        while True:
            vstup = input(f"Zadejte {nazev} pojištěného: ").strip()

            if not vstup:
                print(f"{nazev} musí být vyplněno".capitalize())
                continue
            if not vstup.isalpha():
                print(f"{nazev} musí obsahovat pouze písmena".capitalize())
                continue

            return vstup

    def vstup_ziskej_vek(self):
        """
        Získává od uživatele věk pro vstup
        """
        while True:
            ziskej_vek = input("Zadejte věk: ").strip()
            try:
                vek = int(ziskej_vek)
                if vek < 0:
                    print("Věk musí být kladné číslo")
                    continue
            except ValueError:
                print("Věk musí být kladné číslo")
                continue
            return vek

    def vstup_ziskej_telefon(self):
        """
        Získává od uživatele telefonní číslo pro vstup
        """
        while True:
            ziskej_telefon = input("Zadejte telefonní číslo: ").strip()

            if not ziskej_telefon:
                print("Telefonní číslo musí být vyplněno")
                continue
            if not self.FORMAT_TELEFONU.match(ziskej_telefon):
                print("Nesprávná hodnota pro telefonní číslo")
                continue

            return ziskej_telefon


class UzivatelskeRozhrani:
    """
    Třída zpracovávající volby od uživatele
    """

    validator = ValidatorVstupu()

    def __init__(self, zdroj_dat):
        """
        Inicializační metoda pro vytvoření instance UzivatelskeRozhrani

        :param zdroj_dat: Zdroj dat, s nímž bude třída pracovat
        """
        self.zdroj_dat = zdroj_dat

    def ziskej_vstup(self):
        """
        Získává vstup od uživatele a provádí příslušné akce
        """
        while True:
            print(
                "\n------------------------------\nEVIDENCE POJIŠTĚNÝCH\n------------------------------"
            )
            print(
                "\nVyberte akci:\n\n1 - Přidat nového pojištěného\n2 - Vypiš všechny pojištěné\n3 - Vyhledat pojištěného\n4 - Konec\n"
            )

            volba_vstupu = input("Vaše volba: ")
            if volba_vstupu == "1":
                self.volba_vytvoreni_pojisteneho()
            elif volba_vstupu == "2":
                self.volba_zobrazeni_vsech_pojistenych()
            elif volba_vstupu == "3":
                self.volba_vyhledani_pojisteneho()
            elif volba_vstupu == "4":
                break
            elif volba_vstupu == "X":
                self.volba_vymaz_data()
            else:
                input(
                    "Zadaná nesprávna hodnota pro výběr, pokračujte libovolnou klávesou...\n"
                )

    def volba_vymaz_data(self):
        """
        Volba uživatele pro smazání všech záznamů v databázi
        """
        try:
            self.zdroj_dat.vymaz_vsechny_pojistene()
            print("\nVšechny záznamy byly úspěšně smazány")
        except Exception:
            raise "\nChyba při mazání všech záznamů"

    def volba_vytvoreni_pojisteneho(self):
        """
        Volba uživatele pro vytvoření nového pojištěného
        """
        zadane_jmeno = self.validator.vstup_ziskej_jmeno(nazev="jméno")
        zadane_prijmeni = self.validator.vstup_ziskej_jmeno(nazev="přijmení")
        zadany_vek = self.validator.vstup_ziskej_vek()
        zadany_telefon = self.validator.vstup_ziskej_telefon()

        self.novy_pojisteny = Osoba(
            zadane_jmeno,
            zadane_prijmeni,
            zadany_vek,
            zadany_telefon,
        )

        try:
            if self.novy_pojisteny:
                print(
                    f"\nPojištěný:\n{self.novy_pojisteny}\nbyl úspěšně přidán do databáze"
                )
        except Exception:
            raise "\nChyba při vkládání do databáze"

        return self.zdroj_dat.pridej_pojisteneho_do_evidence(self.novy_pojisteny)

    def zobraz_pojistne(self, seznam_osob):
        """
        Obsahuje seznam pojištěných osob

        :param seznam_osob: Seznam objektů Osoba
        """
        if not seznam_osob:
            print("*** Nenalezené žádné osoby")
        for osoba in seznam_osob:
            print(osoba)

    def volba_zobrazeni_vsech_pojistenych(self):
        """
        Volba uživatele pro zobrazení všech pojištěných osob
        """
        try:
            print("Pojištěné osoby:\n")
            return self.zobraz_pojistne(self.zdroj_dat.vrat_vsechny_pojistene())
        except Exception:
            raise "\nChyba při načtení dat z databáze"

    def volba_vyhledani_pojisteneho(self, nalezene_osoby=None):
        """
        Volba uživatele pro vyhledání pojištěného podle zadaných kritérií
        """
        hledane_jmeno = input("Zadejte jméno pojištěného: ").strip()
        hledane_prijmeni = input("Zadejte příjmení pojištěného: ").strip()

        try:
            if not nalezene_osoby:
                print(
                    f'*** Nenalezená shoda "{hledane_jmeno}" a "{hledane_prijmeni}" v databázi'
                )

            print("Výsledek hledání:\n")
            return self.zobraz_pojistne(
                self.zdroj_dat.vyhledej_pojistene(hledane_jmeno, hledane_prijmeni)
            )
        except Exception:
            raise "\nChyba při vyhledávání pojištěných"
