#include <iostream>

using namespace std;

int main() {
    int first;
    int second;
    int aux;

    cin >> first;
    cin >> second;
    while (second > 0) {
        aux = first % second;
        first = second;
        second = aux;
    }
    cout << first;

    return 0;
}
