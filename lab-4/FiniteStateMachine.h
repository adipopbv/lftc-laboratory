#include <iostream>
#include <vector>
#include <string>
#include <set>
#include "Transition.h"

using namespace std;

class FiniteStateMachine {
private:
    vector<string> alphabet;
    string initialState;
    vector<Transition> transitions;
    vector<string> states;
    vector<string> finalStates;
public:
    FiniteStateMachine(const vector<string> &alphabet, const vector<string> &states, string initialState,
                       const vector<Transition> &transitions, const vector<string> &finalStates);

    const vector<string> &getAlphabet() const;

    const vector<Transition> &getTransitions() const;

    const vector<string> &getFinalStates() const;

    const vector<string> &getStates() const;

    bool checkSequence(string sequence);

    string getLongestPrefix(string sequence);
};
