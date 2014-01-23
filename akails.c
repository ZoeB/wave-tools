/* Impulse Tracker file lister, by Zoe Blade */

#include <stdio.h>

char akaiiToAscii(char character) {
	/* Based on the table at http://web.archive.org/web/20050212062331/http://www.abel.co.uk/~maxim/akai/akaiinfo.htm#4 */
	if (character < 10) {
		return character + 48; /* 0 - 9 */
	} else if (character < 11) {
		return ' ';
	} else if (character < 37) {
		return character + 54; /* A - Z */
	} else if (character < 38) {
		return '#';
	} else if (character < 39) {
		return '+';
	} else if (character < 40) {
		return '-';
	} else if (character < 41) {
		return '.';
	} else {
		return '\0';
	}
}

void describeFile(FILE *inputFilePointer, FILE *outputFilePointer) {
	int character;

	while ((character = getc(inputFilePointer)) != EOF) {
		putc(akaiiToAscii(character), outputFilePointer);
	}

	return;
}

/* This is mostly ripping off K&R's ANSI C, page 162, "Cat". */

int main(int argc, char *argv[]) {
	FILE *filePointer;

	if (argc == 1) {
		describeFile(stdin, stdout);
	} else {
		while (--argc > 0) {
			filePointer = fopen(*++argv, "r");

			if (filePointer == NULL) {
				continue;
			}

			describeFile(filePointer, stdout);
			fclose(filePointer);
		}
	}

	return 0;
}
