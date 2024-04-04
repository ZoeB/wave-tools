/* BPM to semitone converter, for ANSI C, by Zoe Blade, 2024-04-04 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void beatsPerMinuteToSemitones(int beatsPerMinute) {
	float millisecondsPerBeat;
	int semitones;

	/*
	 * The old tempo * 2 ^^ (the pitch change in semitones / 12) = the new tempo
	 */

	millisecondsPerBeat = 60000.0 / beatsPerMinute;

	for (semitones = -2; semitones < 3; semitones++) {
		printf("%3d\t   %2d\t%7.2f\n", beatsPerMinute, semitones, beatsPerMinute * pow(2, semitones / 12.0));
	}

	return;
}

int main(int argc, char *argv[]) {
	int beatsPerMinute;

	printf("BPM\tSts\tBPM\n");
	printf("===\t===\t===\n\n");

	if (argc == 1) {
		for (beatsPerMinute = 80; beatsPerMinute < 145; beatsPerMinute += 5) {
			beatsPerMinuteToSemitones(beatsPerMinute);
		}
	} else {
		beatsPerMinuteToSemitones(atoi(argv[1]));
	}

	return 0;
}
