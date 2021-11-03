#include "Transition.h"

#include <utility>

Transition::Transition(string sourceState, string destinationState, string value) : value(std::move(value)),
                                                                                    sourceState(std::move(sourceState)),
                                                                                    destinationState(std::move(destinationState)) {

}

const string &Transition::getValue() const {
    return value;
}

const string &Transition::getSourceState() const {
    return sourceState;
}

const string &Transition::getDestinationState() const {
    return destinationState;
}
