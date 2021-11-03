#include "FiniteStateMachine.h"

#include <algorithm>

FiniteStateMachine::FiniteStateMachine(const vector<string> &alphabet, const vector<string> &states,
                                       string initialState,
                                       const vector<Transition> &transitions, const vector<string> &finalStates)
        : alphabet(alphabet),
          states(states),
          initialState(std::move(initialState)),
          transitions(transitions),
          finalStates(finalStates) {

}

const vector<string> &FiniteStateMachine::getAlphabet() const {
    return alphabet;
}

const vector<Transition> &FiniteStateMachine::getTransitions() const {
    return transitions;
}

const vector<string> &FiniteStateMachine::getFinalStates() const {
    return finalStates;
}

const vector<string> &FiniteStateMachine::getStates() const {
    return states;
}

bool FiniteStateMachine::checkSequence(string sequence) {
    string prefix;
    string currentState = initialState;
    bool ok;

    while (!sequence.empty()) {
        ok = false;
        for (const auto& transition: transitions) {
            if (transition.getSourceState() == currentState &&
                transition.getValue() == sequence.substr(0, transition.getValue().length())) {
                prefix += transition.getValue();
                sequence.erase(0, transition.getValue().length());
                currentState = transition.getDestinationState();
                ok = true;
                break;
            }
        }
        if (!ok)
            return false;
    }
    if (find(finalStates.begin(), finalStates.end(), currentState) != finalStates.end())
        return true;
    return false;
}

string FiniteStateMachine::getLongestPrefix(string sequence) {
    string prefix;
    string currentState = initialState;
    bool ok;

    while (!sequence.empty()) {
        ok = false;
        for (const auto& transition: transitions) {
            if (transition.getSourceState() == currentState &&
                transition.getValue() == sequence.substr(0, transition.getValue().length())) {
                prefix += transition.getValue();
                sequence.erase(0, transition.getValue().length());
                currentState = transition.getDestinationState();
                ok = true;
                break;
            }
        }
        if (!ok)
            return prefix;
    }
    return prefix;
}