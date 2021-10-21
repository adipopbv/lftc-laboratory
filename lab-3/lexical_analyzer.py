import re

from binary_search_tree import BinarySearchTree


class LexicalAnalyzer:
    def __init__(self, source_code: []) -> None:
        self.atoms = {}
        self.identifiers = BinarySearchTree()
        self.constants = BinarySearchTree()
        self.internal_form = []
        self._source_code = source_code
        self._regex_patterns = {
            "#include": "#include", "<iostream>": "<iostream>", "using": "using",
            "namespace": "namespace", "std": "std", "int": "int",
            "main()": "main\\(\\)", "struct": "struct", "float": "float", "cin": "cin",
            "cout": "cout", "endl": "endl", "if": "if", "else": "else",
            "while": "while", "return": "return", "+": "\\+", "-": "-", "*": "\\*",
            "/": "\\/", "%": "%", "=": "=", "==": "==", ">=": ">=", "<=": "<=",
            ">>": ">>", "<<": "<<", ">": ">", "<": "<", "!": "!", "(": "\\(",
            ")": "\\)", "{": "{", "}": "}", ";": ";", ",": ","}

    def analyze(self) -> None:
        self._source_code = re.sub(r"\n", "\n", self._source_code)
        self._source_code = re.sub(r"\s\s+", " ", self._source_code)
        print(self._source_code)
        while len(self._source_code) > 0:
            split = self._source_code.split(maxsplit=1)
            word = split[0]
            if len(split) > 1:
                self._source_code = split[1]
            else:
                self._source_code = ""
            if re.search(";", word):
                self._add_atom(";")
                word = word[:-1]
            elif re.search(",", word):
                self._add_atom(",")
                word = word[:-1]
            is_atom = False
            for atom in self._regex_patterns.keys():
                if re.match(self._regex_patterns[atom], word):
                    self._add_atom(atom)
                    self.internal_form.append([self.atoms[atom], "-"])
                    is_atom = True
                    break
            if not is_atom:
                if re.match("^[0-9]+$", word) or re.match("^[0-9]+\\.[0-9]+$", word):
                    self._add_atom("CONST")
                    constant_key = self._add_constant(word)
                    self.internal_form.append([self.atoms["CONST"], constant_key])
                elif re.match("^[a-zA-Z][a-zA-Z0-9_-]{0,7}$", word):
                    self._add_atom("ID")
                    identifier_key = self._add_identifier(word)
                    self.internal_form.append([self.atoms["ID"], identifier_key])
                else:
                    raise Exception("error while processing: " + word)

    def _add_atom(self, atom: str):
        if atom not in self.atoms.keys():
            self.atoms[atom] = len(self.atoms)

    def _add_identifier(self, identifier: str):
        key = self.identifiers.get_key_of(identifier)
        if key == -1:
            return self.identifiers.add(identifier)
        return key

    def _add_constant(self, constant: str):
        key = self.constants.get_key_of(constant)
        if key == -1:
            return self.constants.add(constant)
        return key
