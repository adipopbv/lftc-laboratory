import re


def swap_characters(string: str, i: int, j: int) -> str:
    c = list(string)
    c[i], c[j] = c[j], c[i]
    new_string = ''.join(c)
    return new_string


def stari_egale(starea1: list, starea2: list) -> bool:
    if len(starea1) != len(starea2):
        return False
    check = True
    for regula1, regula2 in zip(starea1, starea2):
        if regula1.membru_stang != regula2.membru_stang:
            check = False
        if regula1.membru_drept != regula2.membru_drept:
            check = False
    return check


def stare_in_lista_de_stari(stare_cautata: list, lista_de_stari: list) -> bool:
    for stare in lista_de_stari:
        if stari_egale(stare, stare_cautata):
            return True
    return False


def indexul_starii_in_colectia_canonica(stare_cautata: list, colectia_canonica: list):
    index = 0
    for stare in colectia_canonica:
        if stari_egale(stare, stare_cautata):
            return index
        index += 1
    return None


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
                if regula.membru_drept[index] in self.neterminali and index < len(
                        regula.membru_drept) - 1:
                    if regula.membru_drept[index + 1] in self.terminali:
                        self.follow[regula.membru_drept[index]] += regula.membru_drept[
                            index + 1]
                    else:
                        self.follow[regula.membru_drept[index]] += self.first[
                            regula.membru_drept[index + 1]]
        for regula in self.reguli_de_productie:
            if regula.membru_drept[-1] in self.neterminali:
                for terminal in self.follow[regula.membru_stang]:
                    if terminal not in self.follow[regula.membru_drept[-1]]:
                        self.follow[regula.membru_drept[-1]] += terminal

    def _deplasare(self, index_stare: int, stiva_de_lucru: list, banda_de_intrare: list,
                   banda_de_iesire: list):
        # ceva operatiuni pe ea
        return stiva_de_lucru, banda_de_intrare, banda_de_iesire

    def _reducere(self, index_regula: int):
        pass

    def _accept(self):
        pass

    def _eroare(self):
        pass

    def verifica_secventa(self, fisier_secventa: str) -> list:
        # colectia canonica
        gramatica = []
        for regula_din_stare in self.reguli_de_productie:
            gramatica.append(
                RegulaDeProductie(regula_din_stare.membru_stang, '.' + regula_din_stare.membru_drept))
        starea0 = self._closure([gramatica[0]], gramatica)
        colectia_canonica = [starea0]
        tranzitii = {}
        tabel = {}
        # initializam prima coloana din tabel pt ca starea 0 exista mereu
        for element in self.neterminali + self.terminali + ['$']:
            tabel[element] = [{
                'operation': getattr(self, '_eroare')
            }]
        a_fost_modificat = True
        while a_fost_modificat:
            a_fost_modificat = False
            index_stare = 0
            for stare in colectia_canonica:
                for element in self.neterminali + self.terminali:
                    stare_noua = self._goto(stare, element, gramatica)
                    if stare_noua is not None:
                        index_stare_noua = indexul_starii_in_colectia_canonica(
                            stare_noua, colectia_canonica)
                        if index_stare not in tranzitii or index_stare_noua not in \
                                tranzitii[index_stare]:
                            if not stare_in_lista_de_stari(
                                    stare_noua,
                                    colectia_canonica):
                                # nu exista starea in colectie
                                a_fost_modificat = True
                                colectia_canonica.append(stare_noua)
                                # adaugam coloana noua in tabel
                                for element_tabel in \
                                        self.neterminali + \
                                        self.terminali + \
                                        ['$']:
                                    tabel[element_tabel].append({
                                        'operation': getattr(self, '_eroare')
                                    })
                            # (cel putin acum) exista starea in colectie
                            if 'starea' in tabel[element][index_stare]:
                                # conflict
                                print('Conflict frate')
                                # exit(1)
                            # bagam in tabel operatiunea noua
                            index_stare_noua = indexul_starii_in_colectia_canonica(
                                stare_noua, colectia_canonica)
                            tabel[element][index_stare] = {
                                'operation': getattr(self, '_deplasare'),
                                'starea': index_stare_noua
                            }
                            if index_stare not in tranzitii:
                                tranzitii[index_stare] = []
                            tranzitii[index_stare].append(index_stare_noua)
                # gasim regula cu punct la final pt a pune reducere
                gasita_cu_punct = False
                for regula_din_stare in stare:
                    if regula_din_stare.membru_drept[-1] == '.':
                        # am gasit una cu punct
                        if gasita_cu_punct is True:
                            print('Conflict frate (2 chiar)')
                            exit(2)
                        gasita_cu_punct = True
                        index_regula = 0
                        for regula in self.reguli_de_productie:
                            if regula_din_stare.membru_drept == regula.membru_drept + '.' and \
                                    regula_din_stare.membru_stang == regula.membru_stang:
                                # am gasit-o
                                if regula_din_stare.membru_stang == self.simbol_initial:
                                    # e caz de accept
                                    for element in self.follow[self.simbol_initial]:
                                        tabel[element][index_stare] = {
                                            'operation': getattr(self, '_accept')
                                        }
                                else:
                                    # e caz de reducere
                                    for element in self.follow[regula_din_stare.membru_stang]:
                                        tabel[element][index_stare] = {
                                            'operation': getattr(self, '_reducere'),
                                            'regula': index_regula
                                        }
                                break
                            index_regula += 1
                index_stare += 1

        # (0, abc, )
        stiva_de_lucru = ['0']
        banda_de_intrare = []
        banda_de_iesire = []
        with open(fisier_secventa, 'r') as fisier:
            for element in fisier.readline():
                banda_de_intrare.append(element)

        return []

    def _closure(self, elemente_de_analiza: list, gramatica: list):
        stare = elemente_de_analiza
        a_fost_modificat = True
        while a_fost_modificat:
            a_fost_modificat = False
            for regula_din_stare in stare:
                neterminal = re.search('.*\\.([A-Z]).*', regula_din_stare.membru_drept)
                if neterminal is not None:
                    neterminal = neterminal.group(1)
                    for regula in gramatica:
                        if regula.membru_stang == neterminal and regula not in stare:
                            a_fost_modificat = True
                            stare.append(regula)
        return stare

    def _goto(self, stare, element, gramatica):
        reguli = []
        for regula in stare:
            neterminal = re.search('\\.(' + element + ')', regula.membru_drept)
            if neterminal is not None:
                reguli.append(RegulaDeProductie(
                    regula.membru_stang,
                    swap_characters(
                        regula.membru_drept,
                        neterminal.start(),
                        neterminal.end() - 1)))
        if not reguli:
            return None
        return self._closure(reguli, gramatica)


if __name__ == '__main__':
    gramatica = Gramatica('gramatica2.txt')
    sirul_productiilor_utilizate = gramatica.verifica_secventa('secventa.txt')
    print(sirul_productiilor_utilizate)
    # for regula in gramatica.reguli_de_productie:
    #     print(f'{regula.membru_stang} -> {regula.membru_drept}')
