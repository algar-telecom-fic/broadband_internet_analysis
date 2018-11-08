#include <bits/stdc++.h>
using namespace std;

int main() {
	int n, x; scanf("%d %d", &n, &x);
	for (int i = 0; i < x; ++i) {
		for (int j = 0; j < x; ++j) {
			if (n == 1 and j > i)
				break;
			printf("#");
		}
		puts("");
	}
	return 0;
}