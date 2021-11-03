#include <string>

using namespace std;

class Transition {
private:
    string value;
    string sourceState;
    string destinationState;
public:
    Transition(string sourceState, string destinationState, string value);

    const string &getValue() const;

    const string &getSourceState() const;

    const string &getDestinationState() const;
};
