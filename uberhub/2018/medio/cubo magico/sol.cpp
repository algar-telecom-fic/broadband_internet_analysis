#include <bits/stdc++.h>
using namespace std;

const int N = 3;

int main() {
	const vector< pair<int, int> > pos = {{0, 1}, {1, 0}, {1, 1}, {1, 2}, {2, 1}};
	vector< vector<int> > v;
	v.resize(N);
	for (int i = 0; i < N; ++i)
		v[i].resize(N);
	for (int i = 0; i < 3; ++i)
		for (int j = 0; j < 3; ++j)
			scanf("%d", &v[i][j]);
	bool ans = true;
	for (int i = 1; i < int(pos.size()); ++i)
		ans &= (v[pos[i].first][pos[i].second] == v[pos[0].first][pos[0].second]);
	return printf("%s\n", ans ? "Cruz formada! Pode continuar!" : "Forme a cruz!"), 0;
}