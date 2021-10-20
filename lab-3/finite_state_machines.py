class State:
    def __init__(self, entry_condition, destination_states: [],
                 is_end_state: bool = False):
        self._entry_condition = entry_condition
        self._destination_states = destination_states
        self._is_end_state = is_end_state

    def can_be_entered(self, entry_value: str) -> bool:
        return self._entry_condition(entry_value)


class AtomFSN:
    def __init__(self):
        self._atoms = [
            "#include", "<iostream>", "using", "namespace", "std", "int", "main()",
            "struct", "float", "cin", "cout", "if", "else", "while", "return",
            "+", "-", "*", "/", "%", "=", "==", ">=", "<=",
            ">", "<", ">>", "<<", "!",
            "(", ")", "{", "}", ";", ","
        ]
        self._init_state, self._states = self._generate_states(self._atoms)

    def _generate_states(self, atoms: []) -> (State, []):
        states = []
        init_state = None
        for atom in atoms:
            previous_state = None
            for letter in reversed(atom):
                current_state = State(lambda entry_value: entry_value == letter, [],
                                      True)
                states.append(
                )
        return init_state, states
