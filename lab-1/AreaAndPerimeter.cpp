#include <iostream>

using namespace std;

int main() {
    float area;
    float perim;
    float radius;
    float pi;

    pi = 3.14;
    cin >> radius;
    perim = 2 * pi * radius;
    area = pi * radius * radius;
    cout << perim;
    cout << endl;
    cout << area;

    return 0;
}
