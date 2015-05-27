#include <math.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
	int i;
	float frequency;

	for (i = 1; i < 89; i++) {
		frequency = pow(2, (i - 49) / 12.0) * 440;
		printf("%d\t%8.3f\n", i, frequency);
	}

	return 0;
}
