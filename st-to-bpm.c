/* Semitone to BPM converter, for ANSI C, by Zoe Blade, 2020-01-16 */

#include <stdio.h>
#include <stdlib.h>

#define SEMITONE 1.059463 /* 2^(1/12), as there are 12 equally
                             logarithmically spaced semitones
                             in an octave */

void semitonesToBeatsPerMinute(int beatsPerMinute) {
	int semitones;
	float shiftedBeatsPerMinute;

	/*
	 * MS per beat = 60 seconds / BPM * 1000 MS in a second
	 *             = 60000 MS per minute / BPM
	 */

	for (semitones = -2; semitones < 3; semitones++) {
		if (semitones > 0) {
			/* Going up */
			shiftedBeatsPerMinute = beatsPerMinute * (semitones * SEMITONE);
		} else if (semitones == 0) {
			/* Staying still */
			shiftedBeatsPerMinute = beatsPerMinute;
		} else {
			/* Going down */
			shiftedBeatsPerMinute = beatsPerMinute / ((semitones * -1) * SEMITONE);
		}

		printf("%3d\t       %+1d\t%7.3f\n", beatsPerMinute, semitones, shiftedBeatsPerMinute);
	}

	return;
}

int main(int argc, char *argv[]) {
	int beatsPerMinute;

	printf("BPM\tSemitones\tBPM\n");
	printf("===\t=========\t===\n\n");

	if (argc == 1) {
		for (beatsPerMinute = 80; beatsPerMinute < 145; beatsPerMinute += 5) {
			semitonesToBeatsPerMinute(beatsPerMinute);
		}
	} else {
		semitonesToBeatsPerMinute(atoi(argv[1]));
	}

	return 0;
}
