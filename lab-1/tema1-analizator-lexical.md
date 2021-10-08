# Tema Lab 1

> Limbaj ales: **C++**  
> Conditiile: **a, b, b**

## Specificarea mini-limbajului de programare

\<program> --> #include \<iostream> using namespace std; int main() { [<declarations_list>] [\<instructions_list>] \<return_instruction> }

\<declarations_list> --> \<declaration>; \<declarations_list>;

\<declarations_list> --> \<declaration>;

\<declaration> --> \<type> \<identifier>

\<type> --> int | float | string

\<string> --> ".\*"  

\<identifier> --> ^.{1,8}$

\<instructions_list> --> \<instuction>; \<instructions_list>;

\<instructions_list> --> \<instuction>;

\<instuction> --> \<assignment> | \<io> | \<repetitive> | \<conditional>

\<assignment> --> \<identifier> = \<expression>

\<expression> --> \<expression> + | - | * | / | % \<identifier> | CONST

\<expression> --> \<identifier> | CONST + | - | * | / | % \<identifier> | CONST

\<io> --> \<input> | \<output>

\<input> --> cin >> \<identifier>

\<output> --> cout << \<identifier> | endl

\<conditional> --> if (\<condition>) { \<instructions_list> } [else { \<instructions_list> }]

\<repetitive> --> while (\<condition>) { \<instructions_list> }

\<condition> --> \<expression> < | > | >= | <= | == | != \<expression>

\<return_instruction> --> return 0;

## Textele sursa a 3 mini-programe

1. Perimetrul si aria cercului de o raza data

```cpp
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
```

2. Cmmdc a 2 nr naturale

```cpp
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
```

3. Suma a n numere

```cpp
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
```

## Textele sursa a doua programe care contin erori

1. Doua erori conform MLP, care sunt erori si in limbajul original

```cpp
#include <iostream>

using namespace std;

int main() {
    return 0
}
```

2. Doua erori conform MLP, dar care nu sunt erori in limbajul original

```cpp
int main() {
    return 0;
}
```

