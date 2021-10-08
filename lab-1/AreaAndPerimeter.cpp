#include <iostream>

using namespace std;

int main() {
    struct aaa {
        int bbb;
    } ceva{1}, altceva{1};
    ceva = altceva;
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
