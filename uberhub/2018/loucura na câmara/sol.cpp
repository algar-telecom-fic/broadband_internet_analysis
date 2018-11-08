#include <bits/stdc++.h>
using namespace std;

int main() {
	map<char, int> need, have;
	for (const auto &i : "oqueehisso")
		if (isalpha(i))
			++need[i];
	int n; string s; cin >> n >> s;
	for (const auto &i : s)
		++have[i];
	int ans = INT_MAX;
	for (const auto &i : need)
		ans = min(ans, have[i.first] / need[i.first]);
	while (ans-- > 0)
		printf("%s\n", "Da que eu te dou outra!");
	return 0;
}