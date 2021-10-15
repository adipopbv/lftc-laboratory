#include <iostream>

using namespace std;

int main() {
    int n, aux, s, i;

    cin >> n;
    i = 0;
    s = 0;
    while (i < n) {
        cin >> aux;
        s = s + aux;
        i = i + 1;
    }
    cout << s;

    return 0;
}
