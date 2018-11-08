#include <bits/stdc++.h>
using namespace std;

int main() {
	string pass; cin >> pass;
	string s;
	for (int i = 0; i < 3 and cin >> s; ++i)
		if (s == pass)
			return cout << "Porta liberada!" << '\n', 0;
	return cout << "Porta bloqueada!" << '\n', 0;
}