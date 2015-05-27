#include <math.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
	int pitch;
	int modulo;
	char noteLetter[12] = "CCDDEFFGGAAB";
	char noteIntonation[12] = "-#-#--#-#-#-";
	int octave;
	float frequency;

	for (pitch = 1; pitch < 89; pitch++) {
		octave = (pitch + 8) / 12;
		modulo = (pitch + 8) % 12;
		frequency = pow(2, (pitch - 49) / 12.0) * 440;
		printf("%d\t%c%c%d\t%8.3f\n", pitch, noteLetter[modulo], noteIntonation[modulo], octave, frequency);
	}

	return 0;
}
