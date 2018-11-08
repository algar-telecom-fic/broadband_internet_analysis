#include <bits/stdc++.h>
using namespace std;

const int N = 112345;

int query (const int &idx, const vector<int> &bit) {
	int ans = 0;
	for (int i = idx; i > 0; i -= i & (-i))
		ans += bit[i];
	return ans;
}

void update(const int &idx, const int &value, vector<int> &bit) {
	for (int i = idx; i < int(bit.size()); i += i & (-i))
		bit[i] += value;
}

int main() {
	int n; scanf("%d", &n);
	vector<int> v(n), bit(N, 0);
	for (int i = 0; i < n; ++i)
		scanf("%d", &v[i]);
	reverse(v.begin(), v.end());
	long long ans = 0;
	for (int i = 0; i < n; ++i)
		ans += query(v[i] - 1, bit),
		update(v[i], 1, bit);
	return printf("%lld\n", ans), 0;
}