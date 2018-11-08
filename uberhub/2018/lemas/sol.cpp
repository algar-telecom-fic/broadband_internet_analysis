#include <bits/stdc++.h>
using namespace std;

int main() {
	int n, x; scanf("%d %d", &n, &x);
	vector<int> v(n);
	for (int i = 0; i < n; ++i)
		scanf("%d", &v[i]);
	sort(v.begin(), v.end());
	return printf("%d\n", v[x - 1]), 0;
}