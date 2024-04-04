/* BPM to MS converter, for ANSI C, by Zoe Blade, 2015-12-06 */

#include <stdio.h>
#include <stdlib.h>

void beatsPerMinuteToMilliseconds(int beatsPerMinute) {
	float millisecondsPerBeat;
	int sixteenths;

	/*
	 * MS per beat = 60 seconds / BPM * 1000 MS in a second
	 *             = 60000 MS per minute / BPM
	 */

	millisecondsPerBeat = 60000.0 / beatsPerMinute;

	for (sixteenths = 1; sixteenths < 17; sixteenths++) {
		printf("%3d\t   %2d\t%7.2f\n", beatsPerMinute, sixteenths, millisecondsPerBeat / 4 * sixteenths);
	}

	return;
}

int main(int argc, char *argv[]) {
	int beatsPerMinute;

	printf("BPM\t16ths\tMS\n");
	printf("===\t=====\t=======\n\n");

	if (argc == 1) {
		for (beatsPerMinute = 80; beatsPerMinute < 145; beatsPerMinute += 5) {
			beatsPerMinuteToMilliseconds(beatsPerMinute);
		}
	} else {
		beatsPerMinuteToMilliseconds(atoi(argv[1]));
	}

	return 0;
}
