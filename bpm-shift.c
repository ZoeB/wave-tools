/* BPM semitone shifter, to proportionally change tempo and key, for ANSI C, by ZB, 2022 */
/* Based on BPM as pitch tabulator, to tune tempos, for ANSI C, by ZB, 2020 */

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
		newTempo = pow(2, semitone / 12.0) * tempo;
		printf("            %+i\t%7.3f\n", semitone, newTempo);
	}

	return 0;
}
