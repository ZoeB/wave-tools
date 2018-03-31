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

	printf("Pitch #\tName\tHz\n");
	printf("=======\t=======\t========\n\n");

	for (pitch = 1; pitch < 89; pitch++) {
		octave = (pitch + 8) / 12;
		modulo = (pitch + 8) % 12;
		frequency = pow(2, (pitch - 49) / 12.0) * 440;
		printf("%2d\t%c%c%d\t%8.3f\n", pitch + 20, noteLetter[modulo], noteIntonation[modulo], octave, frequency);
	}

	return 0;
}
