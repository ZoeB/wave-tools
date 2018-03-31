/* MIDI note number / human note name / frequency chart carculator, for ANSI C, by Zoe Blade, 2018-03-31 */

/* See https://newt.phys.unsw.edu.au/jw/notes.html */

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
