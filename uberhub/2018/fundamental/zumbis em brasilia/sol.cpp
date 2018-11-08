#include <bits/stdc++.h>
using namespace std;

const int N = 3;

int main() {
	vector<int> need(N), have(N);
	for (int i = 0; i < N; ++i)
		scanf("%d", &need[i]);
	for (int i = 0; i < N; ++i)
		scanf("%d", &have[i]);
	for (int i = 0; i < N; ++i)
		if (need[i] * (i + 1) > have[i])
			return printf("%s\n", "NAO"), 0;
	return printf("%s\n", "SIM"), 0;
}