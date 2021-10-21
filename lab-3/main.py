from binary_search_tree import BinarySearchTree
from lexical_analyzer import LexicalAnalyzer


def print_atoms(atoms: {}):
    print("\nAtoms:")
    for atom_key in atoms.keys():
        print(str(atoms[atom_key]) + " : " + str(atom_key))


def print_identifiers(identifiers: BinarySearchTree):
    print("\nIdentifiers:\n" + identifiers.to_string())


def print_constants(constants: BinarySearchTree):
    print("\nConstants:\n" + constants.to_string())


def print_internal_form(internal_form: []):
    print("\nInternal form:")
    for pair in internal_form:
        print(str(pair[0]) + " : " + str(pair[1]))


if __name__ == '__main__':
    file = open("in1.txt", "r")
    # file = open("in2.txt", "r")
    # file = open("in3.txt", "r")
    source_code = file.read()
    lexical_analyzer = LexicalAnalyzer(source_code[:])
    try:
        lexical_analyzer.analyze()
        print_atoms(lexical_analyzer.atoms)
        print_identifiers(lexical_analyzer.identifiers)
        print_constants(lexical_analyzer.constants)
        print_internal_form(lexical_analyzer.internal_form)
    except Exception as e:
        print(e)
