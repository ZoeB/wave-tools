#include <math.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
	int i;
	int octave;
	float frequency;

	for (i = 1; i < 89; i++) {
		octave = (i + 8) / 12;
		frequency = pow(2, (i - 49) / 12.0) * 440;
		printf("%d\t%d\t%8.3f\n", i, octave, frequency);
	}

	return 0;
}
