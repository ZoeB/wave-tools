/* Pitch tabulator, for ANSI C, by Zoe Blade, 2015-05-27 */

#include <math.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
	int pitch;
	int modulo;
	char noteLetter[12] = "CCDDEFFGGAAB";
	char noteIntonation[12] = "-#-#--#-#-#-";
	int octave;
	float frequency;

	printf("Name\tMIDI #\tHz\n");
	printf("=======\t=======\t========\n\n");

	for (pitch = 1; pitch < 89; pitch++) {
		octave = (pitch + 8) / 12;
		modulo = (pitch + 8) % 12;
		frequency = pow(2, (pitch - 49) / 12.0) * 440;
		printf("%c%c%d\t%7d\t%8.2f\n", noteLetter[modulo], noteIntonation[modulo], octave, pitch + 20, frequency);
	}

	return 0;
}
