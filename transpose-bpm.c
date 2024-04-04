/* BPM transposer, for ANSI C, by Zoe Blade, 2024-04-04 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void transposeBeatsPerMinute(int beatsPerMinute) {
	int semitones;

	/*
	 * The new tempo = the old tempo * 2 ^ (the pitch change in semitones / 12)
	 */

	for (semitones = -2; semitones < 3; semitones++) {
		printf("%3d\t%+3d\t%7.3f\n", beatsPerMinute, semitones, beatsPerMinute * pow(2, semitones / 12.0));
	}

	return;
}

int main(int argc, char *argv[]) {
	int beatsPerMinute;

	printf("BPM\tSts\tBPM\n");
	printf("===\t===\t=======\n\n");

	if (argc == 1) {
		for (beatsPerMinute = 80; beatsPerMinute < 145; beatsPerMinute += 5) {
			transposeBeatsPerMinute(beatsPerMinute);
		}
	} else {
		transposeBeatsPerMinute(atoi(argv[1]));
	}

	return 0;
}
