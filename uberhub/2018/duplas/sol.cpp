#include <bits/stdc++.h>
using namespace std;

bool valid(const string &a, const string &b) {
	map<char, int> kappa, keepo;
	for (const auto &i : a)
		++kappa[i];
	for (const auto &i : b)
		++keepo[i];
	bool ans1 = true;
	for (const auto &i : kappa)
		if (keepo[i.first] < kappa[i.first])
			ans1 = false;
	bool ans2 = true;
	for (const auto &i : keepo)
		if (kappa[i.first] < keepo[i.first])
			ans2 = false;
	return ans1 | ans2;
}

int main() {
	string a, b; cin >> a >> b;
	if (valid(a, b))
		return cout << a << " e " << b << " formam uma boa dupla" << '\n', 0;
	return cout << "nao vai dar certo" << '\n', 0;
}