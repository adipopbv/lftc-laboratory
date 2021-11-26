class RegulaDeProductie:
    membru_stang = ''
    membru_drept = ''

    def __init__(self, membru_stang: str, membru_drept: str):
        self.membru_stang = membru_stang
        self.membru_drept = membru_drept


class Gramatica:
    reguli_de_productie = []
    simbol_initial = ''

    def __init__(self, fisier_gramatica: str):
        self._citeste_fisier(fisier_gramatica)
        self.simbol_initial = self.reguli_de_productie[0].membru_stang

    def _citeste_fisier(self, fisier_gramatica: str):
        with open(fisier_gramatica, 'r') as fisier:
            for linie in fisier.readlines():
                cuvinte = linie.strip().split(' ')
                self.reguli_de_productie.append(
                    RegulaDeProductie(cuvinte[0], cuvinte[2])
                )

    def gaseste_regulile_cu_simbolul_initial_in_dreapta(self):
        reguli = []
        for regula_de_productie in self.reguli_de_productie:
            if self.simbol_initial in regula_de_productie.membru_drept:
                reguli.append(regula_de_productie)
        return reguli


if __name__ == '__main__':
    gramatica = Gramatica('gramatica.txt')
    reguli_de_productie = gramatica.gaseste_regulile_cu_simbolul_initial_in_dreapta()
    for regula in reguli_de_productie:
        print(f'{regula.membru_stang} -> {regula.membru_drept}')
