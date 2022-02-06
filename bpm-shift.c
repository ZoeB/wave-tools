/* BPM as pitch tabulator, to tune tempos, for ANSI C, by ZB, 2020 */
/* Based on pitch tabulator, for ANSI C, by Zoe Blade, 2015, 2018 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	int semitone;
	float tempo;
	float newTempo;

	if (argc != 2) {
		printf("Please specify a tempo\n");
		return 1;
	}

	tempo = atof(argv[1]);
	printf("Semitone shift\tBPM\n");
	printf("==============\t=======\n\n");

	for (semitone = -5; semitone <= 5; semitone++) {
		newTempo = pow(2, (semitone - 49) / 12.0) * 440;
		printf("            %+i\t%7.3f\n", semitone, newTempo);
	}

	return 0;
}
