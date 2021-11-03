#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "FiniteStateMachine.h"

using namespace std;

string fileName = "constants.txt";

void splitLine(vector<string> &words, string line) {
    while (!line.empty()) {
        string word = line.substr(0, line.find(','));
        words.push_back(word);
        line.erase(0, word.length() + 1);
    }
}

void readFromFile(vector<string> &alphabet, vector<string> &states, string &initialState, vector<string> &finalStates,
                  vector<Transition> &transitions) {
    string line;
    ifstream fin(fileName);

    getline(fin, line);
    splitLine(alphabet, line);

    getline(fin, line);
    splitLine(states, line);

    fin >> initialState;
    fin.get();

    getline(fin, line);
    splitLine(finalStates, line);

    while (!fin.eof()) {
        getline(fin, line);
        string sourceState = line.substr(0, line.find(','));
        line.erase(0, sourceState.length() + 1);
        string destinationState = line.substr(0, line.find(','));
        line.erase(0, sourceState.length() + 1);
        string value = line;

        transitions.emplace_back(sourceState, destinationState, value);
    }
}

void readFromCmd(vector<string> &alphabet, vector<string> &states, string &initialState, vector<string> &finalStates,
                 vector<Transition> &transitions) {
    string line;
    int n;

    cout << "The states alphabet: ";
    cin >> line;
    splitLine(alphabet, line);

    cout << "The states: ";
    cin >> line;
    splitLine(states, line);

    cout << "The initial state: ";
    cin >> initialState;

    cout << "The final states: ";
    cin >> line;
    splitLine(finalStates, line);

    cout << "The transitions count: ";
    cin >> n;
    cout << "The transition's source, destination and value: ";
    for (int i = 0; i < n; i++) {
        cin >> line;
        string sourceState = line.substr(0, line.find(','));
        line.erase(0, sourceState.length() + 1);
        string destinationState = line.substr(0, line.find(','));
        line.erase(0, sourceState.length() + 1);
        string value = line;

        transitions.emplace_back(sourceState, destinationState, value);
    }
}

void printStates(const FiniteStateMachine &finiteStateMachine) {
    cout << "The states: ";
    for (const auto& state: finiteStateMachine.getStates())
        cout << state << " ";
    cout << "\n";
}

void printAlphabet(const FiniteStateMachine& finiteStateMachine) {
    cout << "The alphabet: ";
    for (const auto& letter: finiteStateMachine.getAlphabet())
        cout << letter << " ";
    cout << "\n";
}

void printTransitions(const FiniteStateMachine& finiteStateMachine) {
    cout << "The transitions:\n";
    for (const auto& transition: finiteStateMachine.getTransitions())
        cout << "   " << transition.getSourceState() << " " << transition.getDestinationState() << " " <<
             transition.getValue() << "\n";
}

void printFinalStates(const FiniteStateMachine& finiteStateMachine) {
    cout << "The final states: ";
    for (const auto& finalState: finiteStateMachine.getFinalStates())
        cout << finalState << " ";
    cout << "\n";
}

void checkSequence(FiniteStateMachine finiteStateMachine) {
    string line;
    cout << "Sequence to check: ";
    cin >> line;
    if (finiteStateMachine.checkSequence(line))
        cout << "Valid sequence\n";
    else
        cout << "Invalid sequence\n";
}

void printLongestPrefix(FiniteStateMachine finiteStateMachine) {
    string line;
    cout << "Sequence to process: ";
    cin >> line;
    string prefix = finiteStateMachine.getLongestPrefix(line);
    if (prefix.empty())
        cout << "There is no valid prefix\n";
    else
        cout << prefix << "\n";
}

void printReadCommands() {
    cout << "   0 - Exit\n";
    cout << "   1 - Read from file\n";
    cout << "   2 - Read from the command line\n\n";
}

void printCommands() {
    cout << "Options:\n";
    cout << "   0 - Exit\n";
    cout << "   1 - The states\n";
    cout << "   2 - The alphabet\n";
    cout << "   3 - The transitions\n";
    cout << "   4 - The final states\n";
    cout << "   5 - Check sequence validity\n";
    cout << "   6 - Longest prefix of an accepted sequence\n";
}

int main() {
    vector<string> alphabet;
    vector<string> states;
    string initialState;
    vector<Transition> transitions;
    vector<string> finalStates;

    int command;
    cout << "Hello there!\n\nPlease choose one of the following:\n";
    printReadCommands();
    cout << "> ";
    cin >> command;
    switch (command) {
        case 0:
            exit(0);
        case 1:
            readFromFile(alphabet, states, initialState, finalStates, transitions);
            break;
        case 2:
            readFromCmd(alphabet, states, initialState, finalStates, transitions);
            break;
        default: {
            cout << "Invalid command!\n";
            exit(0);
        }
    }

    FiniteStateMachine finiteStateMachine = FiniteStateMachine(alphabet, states, initialState, transitions,
                                                               finalStates);
    while (true) {
        printCommands();
        cout << "> ";
        cin >> command;
        switch (command) {
            case 0:
                exit(0);
            case 1:
                printStates(finiteStateMachine);
                break;
            case 2:
                printAlphabet(finiteStateMachine);
                break;
            case 3:
                printTransitions(finiteStateMachine);
                break;
            case 4:
                printFinalStates(finiteStateMachine);
                break;
            case 5:
                checkSequence(finiteStateMachine);
                break;
            case 6:
                printLongestPrefix(finiteStateMachine);
                break;
            default: {
                cout << "Invalid command!\n";
                return 0;
            }
        }
        cout << "\n";
    }
}
