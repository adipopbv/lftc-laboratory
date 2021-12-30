import copy
import re


class RegexString(str):
    def re_eq(self, other):
        if re.match(str(self), other):
            return True
        return False


def swap_elements(list_of_elements: list, i: int, j: int) -> list:
    new_list = copy.deepcopy(list_of_elements)
    new_list[i], new_list[j] = new_list[j], new_list[i]
    return new_list


def equal_lists(list1: list, list2: list) -> bool:
    if len(list1) != len(list2):
        return False
    for element1, element2 in zip(list1, list2):
        if element1 != element2:
            return False
    return True


def consecutive_elements_in_list(elements_list: list, element1: str,
                                 element2: str) -> int:
    for index in range(0, len(elements_list) - 1):
        if elements_list[index] == element1 and elements_list[index + 1] == element2:
            return index
    return -1


def stari_egale(starea1: list, starea2: list) -> bool:
    if len(starea1) != len(starea2):
        return False
    check = True
    for regula1, regula2 in zip(starea1, starea2):
        if regula1.membru_stang != regula2.membru_stang:
            check = False
        if not equal_lists(regula1.membru_drept, regula2.membru_drept):
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
    membru_drept = []

    def __init__(self, membru_stang: str, membru_drept: list):
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
            RegulaDeProductie("Q", [self.reguli_de_productie[0].membru_stang])
        )
        self.simbol_initial = "Q"

    def _citeste_fisier(self, fisier_gramatica: str):
        with open(fisier_gramatica, 'r') as fisier:
            for linie in fisier.readlines():
                cuvinte = linie.strip().split(' ')
                membrul_drept = cuvinte[2:]
                if cuvinte[0] == '<ID>' or cuvinte[0] == '<CONST>':
                    membrul_drept = [RegexString(cuvinte[2])]
                self.reguli_de_productie.append(
                    RegulaDeProductie(cuvinte[0], membrul_drept)
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
                    if regula.membru_drept[0] not in self.first[regula.membru_stang]:
                        self.first[regula.membru_stang].append(regula.membru_drept[0])
            else:
                self.first[regula.membru_stang] = []
        a_fost_modificat = True
        while a_fost_modificat:
            a_fost_modificat = False
            for regula in self.reguli_de_productie:
                if regula.membru_drept[0] in self.neterminali:
                    for element in self.first[regula.membru_drept[0]]:
                        if element not in self.first[regula.membru_stang]:
                            a_fost_modificat = True
                            self.first[regula.membru_stang].append(element)

    def _gaseste_follow(self):
        for neterminal in self.neterminali:
            if neterminal == self.simbol_initial:
                self.follow[neterminal] = ['$']
            else:
                self.follow[neterminal] = []
        for regula in self.reguli_de_productie:
            for index in range(0, len(regula.membru_drept)):
                if regula.membru_drept[index] in self.neterminali and index < len(
                        regula.membru_drept) - 1:
                    # urmeaza un terminal
                    if regula.membru_drept[index + 1] in self.terminali:
                        if regula.membru_drept[index + 1] not in \
                                self.follow[regula.membru_drept[index]]:
                            self.follow[regula.membru_drept[index]].append(
                                regula.membru_drept[index + 1])
                    # urmeaza un neterminal
                    else:
                        for element in self.first[regula.membru_drept[index + 1]]:
                            if element not in self.follow[regula.membru_drept[index]]:
                                self.follow[regula.membru_drept[index]].append(element)
        for regula in self.reguli_de_productie:
            if regula.membru_drept[-1] in self.neterminali:
                for terminal in self.follow[regula.membru_stang]:
                    if terminal not in self.follow[regula.membru_drept[-1]]:
                        self.follow[regula.membru_drept[-1]].append(terminal)

    def _deplasare(self, index_stare: int, stiva_de_lucru: list, banda_de_intrare: list,
                   banda_de_iesire: list):
        stiva_de_lucru.append(banda_de_intrare[0])
        stiva_de_lucru.append(index_stare)
        banda_de_intrare.pop(0)
        return stiva_de_lucru, banda_de_intrare, banda_de_iesire

    def _reducere(self, index_regula: int, stiva_de_lucru: list, banda_de_intrare: list,
                  banda_de_iesire: list, tabel: dict):
        banda_de_iesire.insert(0, index_regula)
        regula_de_lucru = RegulaDeProductie(
            self.reguli_de_productie[index_regula].membru_stang,
            copy.deepcopy(self.reguli_de_productie[index_regula].membru_drept)
        )
        while stiva_de_lucru and regula_de_lucru.membru_drept:
            element = stiva_de_lucru[-2]
            if (type(regula_de_lucru.membru_drept[-1]) is RegexString and
                regula_de_lucru.membru_drept[-1].re_eq(element)) or element == \
                    regula_de_lucru.membru_drept[-1]:
                stiva_de_lucru.pop()
                stiva_de_lucru.pop()
            regula_de_lucru.membru_drept = regula_de_lucru.membru_drept[:-1]
        stiva_de_lucru.append(regula_de_lucru.membru_stang)
        stiva_de_lucru.append(
            tabel[regula_de_lucru.membru_stang][stiva_de_lucru[-2]]['starea'])
        return stiva_de_lucru, banda_de_intrare, banda_de_iesire

    def _acceptare(self, banda_de_iesire: list):
        print('Secventa acceptata\nSirul productiilor este: ')
        print(banda_de_iesire)
        exit(0)

    def _eroare(self, mesaj: str):
        print(f'Secventa nu e acceptata: {mesaj}')
        exit(3)

    def verifica_secventa(self, fisier_secventa: str):
        # colectia canonica
        gramatica = []
        for regula_din_stare in self.reguli_de_productie:
            noul_membru_drept = copy.deepcopy(regula_din_stare.membru_drept)
            noul_membru_drept.insert(0, '.')
            gramatica.append(
                RegulaDeProductie(regula_din_stare.membru_stang,
                                  noul_membru_drept))
        starea0 = self._closure([gramatica[0]], gramatica)
        colectia_canonica = [starea0]
        tranzitii = {}
        tabel = {}
        # initializam prima coloana din tabel pt ca starea 0 exista mereu
        for element in self.neterminali + self.terminali + ['$']:
            tabel[element] = [{
                'operatie': 'eroare'
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
                                        'operatie': 'eroare'
                                    })
                            # (cel putin acum) exista starea in colectie
                            if 'starea' in tabel[element][index_stare]:
                                # conflict
                                print('Conflict frate')
                                exit(1)
                            # bagam in tabel operatiunea noua
                            index_stare_noua = indexul_starii_in_colectia_canonica(
                                stare_noua, colectia_canonica)
                            tabel[element][index_stare] = {
                                'operatie': 'deplasare',
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
                            noul_membru_drept = copy.deepcopy(regula.membru_drept)
                            noul_membru_drept.append('.')
                            if equal_lists(regula_din_stare.membru_drept,
                                           noul_membru_drept) \
                                    and regula_din_stare.membru_stang == \
                                    regula.membru_stang:
                                # am gasit-o
                                if regula_din_stare.membru_stang == self.simbol_initial:
                                    # e caz de accept
                                    for element in self.follow[self.simbol_initial]:
                                        tabel[element][index_stare] = {
                                            'operatie': 'acceptare'
                                        }
                                else:
                                    # e caz de reducere
                                    for element in \
                                            self.follow[regula_din_stare.membru_stang]:
                                        tabel[element][index_stare] = {
                                            'operatie': 'reducere',
                                            'regula': index_regula
                                        }
                                break
                            index_regula += 1
                index_stare += 1

        stiva_de_lucru = [0]
        banda_de_intrare = []
        banda_de_iesire = []
        with open(fisier_secventa, 'r') as fisier:
            for line in fisier.readlines():
                line = line.strip()
                for element in line.split(' '):
                    if element != '':
                        banda_de_intrare.append(element)
        banda_de_intrare.append('$')

        while True:
            try:
                celula = self._gaseste_celula(banda_de_intrare[0],
                                              stiva_de_lucru[-1],
                                              tabel)
                if celula['operatie'] == 'deplasare':
                    stiva_de_lucru, banda_de_intrare, banda_de_iesire = self._deplasare(
                        celula['starea'], stiva_de_lucru, banda_de_intrare,
                        banda_de_iesire)
                elif celula['operatie'] == 'reducere':
                    stiva_de_lucru, banda_de_intrare, banda_de_iesire = self._reducere(
                        celula['regula'], stiva_de_lucru, banda_de_intrare,
                        banda_de_iesire, tabel)
                elif celula['operatie'] == 'acceptare':
                    self._acceptare(banda_de_iesire)
                else:
                    self._eroare(banda_de_intrare[0])
            except KeyError as e:
                print(f'Secventa nu e acceptata: {e}')
                exit(3)

    def _gaseste_celula(self, element: str, starea_curenta: int, tabel: dict):
        chei_regex_string = []
        for cheie in tabel.keys():
            if type(cheie) is RegexString:
                chei_regex_string.append(cheie)
            elif cheie == element:
                return tabel[cheie][starea_curenta]
        for cheie in chei_regex_string:
            if cheie.re_eq(element):
                return tabel[cheie][starea_curenta]
        raise KeyError(element)

    def _closure(self, elemente_de_analiza: list, gramatica: list):
        stare = elemente_de_analiza
        a_fost_modificat = True
        while a_fost_modificat:
            a_fost_modificat = False
            for regula_din_stare in stare:
                for neterminal in self.neterminali:
                    index = consecutive_elements_in_list(regula_din_stare.membru_drept,
                                                         '.', neterminal)
                    if index != -1:
                        for regula in gramatica:
                            if regula.membru_stang == neterminal and \
                                    regula not in stare:
                                a_fost_modificat = True
                                stare.append(regula)
                        break
        return stare

    def _goto(self, stare, element, gramatica):
        reguli = []
        for regula in stare:
            index = consecutive_elements_in_list(regula.membru_drept, '.', element)
            if index != -1:
                noul_membru_drept = copy.deepcopy(regula.membru_drept)
                reguli.append(RegulaDeProductie(
                    regula.membru_stang,
                    swap_elements(noul_membru_drept, index, index + 1)))
        if not reguli:
            return None
        return self._closure(reguli, gramatica)


if __name__ == '__main__':
    gramatica = Gramatica('gramatica.txt')
    gramatica.verifica_secventa('secventa.txt')
