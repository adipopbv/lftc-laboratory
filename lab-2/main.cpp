#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>

using namespace std;

const vector<string> keywords = {"#include", "<iostream>", "using", "namespace", "std", "int", "main()", "struct", "float", "cin", "cout", "if", "else", "while", "return"};
const vector<string> operators = {"+", "-", "*", "/", "%", "=", "==", ">=", "<=", ">", "<", ">>", "<<", "!"};
const vector<string> delimiters = {"(", ")", "{", "}", ";", ","};

int main() {
    ifstream fin("in2.txt");
    string line;
    set<string> atoms;
    while (!fin.eof()) {
        getline(fin, line);
        // keywords
        for (const auto& atom: keywords) {
            if (line.find(atom) != string::npos) {
                atoms.insert(atom);
                line.erase(line.find(atom), atom.length());
            }
        }
        // operators
        for (const auto& atom: operators) {
            if (line.find(atom) != string::npos) {
                atoms.insert(atom);
                line.erase(line.find(atom), atom.length());
            }
        }
        // delimiters
        for (const auto& atom: delimiters) {
            if (line.find(atom) != string::npos) {
                atoms.insert(atom);
                line.erase(line.find(atom), atom.length());
            }
        }
        // constants
        for (char digit = '0'; digit <= '9'; digit++)
            if (line.find(digit) != string::npos) {
                atoms.insert("CONST");
                break;
            }
        // identifiers
        for (char letter = 'a'; letter <= 'z'; letter++)
            if (line.find(letter) != string::npos || line.find(toupper(letter)) != string::npos) {
                atoms.insert("ID");
                break;
            }
    }
    fin.close();
    for(const auto& atom: atoms)
        cout << atom << "\n";

    return 0;
}
