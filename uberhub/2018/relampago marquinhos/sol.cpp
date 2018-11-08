#include <bits/stdc++.h>
using namespace std;

int main() {
	int n; cin >> n;
	vector< pair<long long, string> > v;
	while (n-- > 0) {
		string s; long long x; cin >> s >> x;
		v.push_back({x, s});
	}
	sort(v.begin(), v.end());
	string goal = "Marquinhos";
	if (v[0].second == goal)
		return cout << "Parabéns!! Você ganhou a corrida!" << '\n', 0;
	for (int i = 0; i < int(v.size()); ++i) {
		if (v[i].second == goal)
			break;
		cout << v[i].second << '\n';
	}
	return 0;
}