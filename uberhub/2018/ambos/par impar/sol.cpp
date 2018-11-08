#include <bits/stdc++.h>
using namespace std;

int main() {
	int n; string s; cin >> n >> s;
	int odd = 0, even = 0, eoq = 0;
	for (const auto &i : s) {
		if (i == '?')
			++eoq;
		else if ((i - '0') & 1)
			++odd;
		else
			++even;
	}
	if (even + eoq <= odd)
		return cout << "Impossivel" << '\n', 0;
	for (int i = 0; i < n; ++i)
		if (s[i] == '?') {
			--eoq;
			if (odd + 1 < even + eoq)
				s[i] = '9',
				++odd;
			else
				s[i] = '8',
				++even;
		}
	return cout << s << '\n', 0;
}