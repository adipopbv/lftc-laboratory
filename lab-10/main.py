class RegulaDeProductie:
    membru_stang = ''
    membru_drept = ''

    def __init__(self, membru_stang: str, membru_drept: str):
        self.membru_stang = membru_stang
        self.membru_drept = membru_drept


class Gramatica:
    reguli_de_productie = []
    simbol_initial = ''
    neterminali = []
    terminali = []
    first = {}
    follow = {}

    def __init__(self, fisier_gramatica: str):
        self._citeste_fisier(fisier_gramatica)
        self._imbogateste_gramatica()
        self._gaseste_neterminali_si_terminali()
        self._gaseste_first()
        self._gaseste_follow()

    def _imbogateste_gramatica(self):
        self.reguli_de_productie.insert(
            0,
            RegulaDeProductie("Q", self.reguli_de_productie[0].membru_stang)
        )
        self.simbol_initial = "Q"

    def _citeste_fisier(self, fisier_gramatica: str):
        with open(fisier_gramatica, 'r') as fisier:
            for linie in fisier.readlines():
                cuvinte = linie.strip().split(' ')
                self.reguli_de_productie.append(
                    RegulaDeProductie(cuvinte[0], cuvinte[2])
                )

    def _gaseste_neterminali_si_terminali(self):
        for regula in self.reguli_de_productie:
            if regula.membru_stang not in self.neterminali:
                self.neterminali.append(regula.membru_stang)
        for regula in self.reguli_de_productie:
            for element in regula.membru_drept:
                if element not in self.neterminali and element not in self.terminali:
                    self.terminali.append(element)

    def _gaseste_first(self):
        for regula in self.reguli_de_productie:
            if regula.membru_drept[0] in self.terminali:
                if regula.membru_stang not in self.first:
                    self.first[regula.membru_stang] = [regula.membru_drept[0]]
                else:
                    self.first[regula.membru_stang].append(regula.membru_drept[0])
            else:
                self.first[regula.membru_stang] = []
        a_fost_modificat = True
        while a_fost_modificat:
            a_fost_modificat = False
            for regula in self.reguli_de_productie:
                if regula.membru_drept[0] in self.neterminali:
                    if not self.first[regula.membru_stang]:
                        a_fost_modificat = True
                        self.first[regula.membru_stang] += \
                            self.first[regula.membru_drept[0]]

    def _gaseste_follow(self):
        # nu mere cu epsilon
        for neterminal in self.neterminali:
            if neterminal == self.simbol_initial:
                self.follow[neterminal] = ['$']
            else:
                self.follow[neterminal] = []
        for regula in self.reguli_de_productie:
            for index in range(0, len(regula.membru_drept)):
                if regula.membru_drept[index] in self.neterminali and index < len(regula.membru_drept) - 1:
                    if regula.membru_drept[index + 1] in self.terminali:
                        self.follow[regula.membru_drept[index]] += regula.membru_drept[index + 1]
                    else:
                        self.follow[regula.membru_drept[index]] += self.first[regula.membru_drept[index + 1]]
        for regula in self.reguli_de_productie:
            if regula.membru_drept[-1] in self.neterminali:
                for terminal in self.follow[regula.membru_stang]:
                    if terminal not in self.follow[regula.membru_drept[-1]]:
                        self.follow[regula.membru_drept[-1]] += terminal

    def verifica_secventa(self, fisier_secventa: str) -> list:
        # (0, abc, )
        stiva_de_lucru = ['0']
        banda_de_intrare = []
        banda_de_iesire = []
        with open(fisier_secventa, 'r') as fisier:
            for element in fisier.readline():
                banda_de_intrare += element

        # if


if __name__ == '__main__':
    gramatica = Gramatica('gramatica.txt')
    sirul_productiilor_utilizate = gramatica.verifica_secventa('secventa.txt')
    print(sirul_productiilor_utilizate)
    # for regula in gramatica.reguli_de_productie:
    #     print(f'{regula.membru_stang} -> {regula.membru_drept}')
