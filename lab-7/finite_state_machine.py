from transition import Transition


class FiniteStateMachine:
    def __init__(self, config_file_name: str):
        self._alphabet = []
        self._states = []
        self._initial_state = None
        self._final_states = []
        self._transitions = []
        self._load_from_file(config_file_name)

    def _load_from_file(self, config_file_name: str) -> None:
        lines = open(config_file_name, "r").readlines()
        self._alphabet = lines[0].rstrip().split(',')
        self._states = lines[1].rstrip().split(',')
        self._initial_state = lines[2].rstrip()
        self._final_states = lines[3].rstrip().split(',')
        self._transitions = []
        for line in lines[4:]:
            words = line.rstrip().split(',')
            self._transitions.append(Transition(words[2], words[0], words[1]))

    def checkSequence(self, sequence: str) -> bool:
        currentState = self._initial_state

        while sequence != '':
            ok = False
            for transition in self._transitions:
                if transition.source_state == currentState and sequence.startswith(
                        transition.value):
                    sequence = sequence.removeprefix(transition.value)
                    currentState = transition.destination_state
                    ok = True
                    break
            if not ok:
                return False
        if currentState in self._final_states:
            return True
        return False
