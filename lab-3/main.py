from binary_search_tree import BinarySearchTree
from finite_state_machines import AtomFSN


class LexicalAnalyzer:
    def __init__(self, code_lines: []) -> None:
        self.atoms = {}
        self.symbol_table = BinarySearchTree()
        self.internal_form = []
        self._code_lines = code_lines
        self._atom_fsn = AtomFSN()

    def analyze(self) -> None:
        """
        Processes the given lines of code into the internal form of the source program

        :return: nothing
        """
        for code_line in self._code_lines:
            pass


if __name__ == '__main__':
    file = open("in.txt", "r")
    lexical_analyzer = LexicalAnalyzer(file.readlines())
    try:
        lexical_analyzer.analyze()
        print(lexical_analyzer.atoms)
        print(lexical_analyzer.symbol_table)
        print(lexical_analyzer.internal_form)
    except Exception as e:
        print(e)
