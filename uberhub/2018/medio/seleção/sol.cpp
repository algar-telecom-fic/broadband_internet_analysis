#include <bits/stdc++.h>
using namespace std;

int main() {
	int n, e; scanf("%d %d", &n, &e);
	int ans = 0;
	while (n-- > 0) {
		int current = 0;
		for (int i = 0; i < 3; ++i) {
			int x; scanf("%d", &x);
			current += x;
		}
		if ((current / 3) >= e)
			++ans;
	}
	return printf("Existe(m) %d candidata(s) estonteante(s)!\n", ans), 0;
}