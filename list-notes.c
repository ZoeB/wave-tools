/* MIDI note number / human note name / frequency chart carculator, for ANSI C, by Zoe Blade, 2018-03-31 */

/* See https://newt.phys.unsw.edu.au/jw/notes.html */

#include <stdio.h>

int main(int argc, char *argv[]) {
	float fundamentalFrequency;
	int octave;
	int semitone;

	printf("MIDI NT Frequency\n"); /* MIDI decimal; note name; frequency */
	for (octave = 0; octave < 8; octave++) {
		for (semitone = 0; semitone < 12; semitone++) {
			printf("%4i\n", 24 + (12 * octave) + semitone);
		}
	}

	return 0;
}
