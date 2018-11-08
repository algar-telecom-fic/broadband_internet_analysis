#include <bits/stdc++.h>
using namespace std;

int main() {
	int n, x; scanf("%d %d", &n, &x);
	int lcm = (n * 100) / __gcd(n, 100);
	int grade = x * (lcm / n);
	int aux = lcm / 100;
	if (grade > 60 * aux)
		return printf("%s\n", "Ta muito feliz!"), 0;
	if (grade < 50 * aux)
		return printf("%s\n", "Ta triste!"), 0;
	return printf("%s\n", "Ta feliz!"), 0;
}