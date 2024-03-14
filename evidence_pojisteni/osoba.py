class Osoba:
    """
    Třída reprezentující pojištěnou osobu v evidenci
    """

    def __init__(self, jmeno, prijmeni, vek, telefon):
        """
        Inicializační metoda pro vytvoření instance Osoba

        :param jmeno (str): Jméno pojištěné osoby
        :param prijmeni (str): Příjmení pojištěné osoby
        :param vek (int): Věk pojištěné osoby
        :param telefon (str): Telefonní číslo pojištěné osoby
        """
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.vek = vek
        self.telefon = telefon

    def __str__(self):
        """
        Vrací textovou reprezentaci pojištěné osoby
        """
        return f"{self.jmeno:<15} {self.prijmeni:<15} {self.vek:<5} {self.telefon}"
