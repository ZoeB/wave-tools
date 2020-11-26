/* BPM as pitch tabulator, to tune tempos, for ANSI C, by ZB, 2020 */
/* Based on pitch tabulator, for ANSI C, by Zoe Blade, 2015, 2018 */
/* Obviously, these are not real MIDI numbers (which are positive,
   between 0 and 127 inclusive), just for reference */

#include <math.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
	int pitch;
	int modulo;
	char noteLetter[12] = "CCDDEFFGGAAB";
	char noteIntonation[12] = "-#-#--#-#-#-";
	int octave;
	float frequency;
	float tempo;

	printf("Name\tMIDI #\tHz\tBPM\n");
	printf("=======\t=======\t=======\t========\n\n");

	for (pitch = -56; pitch < -32; pitch++) {
		octave = (pitch + 8) / 12;
		modulo = (pitch + 8 + 60) % 12; /* Add 60 just to get it in the positive range, to calculate the modulo */
		frequency = pow(2, (pitch - 49) / 12.0) * 440;
		tempo = frequency * 60;
		printf("%c%c%d\t%7d\t%5.3f\t%8.3f\n", noteLetter[modulo], noteIntonation[modulo], octave, pitch + 20, frequency, tempo);
	}

	return 0;
}
