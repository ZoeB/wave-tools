/* Ptolemaic / just intonation calculator, for ANSI C, by Zoe Blade, 2017-02-11 */

/* See https://en.wikipedia.org/wiki/Ptolemy%27s_intense_diatonic_scale */

#include <stdio.h>

int main(int argc, char *argv[]) {
	float fundamentalFrequency;
	int octave;

	printf("Fundamental frequency? ");
	scanf("%f", &fundamentalFrequency);

	for (octave = 1; octave < 3; octave++) {
		printf("\n%9.3f\n", (fundamentalFrequency / 1 * octave));
		printf("%9.3f\n", (fundamentalFrequency / 1 * octave) / 8 * 9);
		printf("%9.3f\n", (fundamentalFrequency / 1 * octave) / 4 * 5);
		printf("%9.3f\n", (fundamentalFrequency / 1 * octave) / 3 * 4);
		printf("%9.3f\n", (fundamentalFrequency / 1 * octave) / 2 * 3);
		printf("%9.3f\n", (fundamentalFrequency / 1 * octave) / 3 * 5);
		printf("%9.3f\n", (fundamentalFrequency / 1 * octave) / 8 * 15);
	}

	return 0;
}
