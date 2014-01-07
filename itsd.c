/* Impulse Tracker sample describer, by Zoe Blade */

/* This is mostly ripping off ANSI C page 162, Cat */

#include <stdio.h>

void describeSample(FILE *ifp, FILE *ofp) {
	int characterNumber = 0;
	int character;

	/* TODO: Fix redundancy in checking if limit's reached */
	while (1) {
		character = getc(ifp);

		if (character == EOF || (characterNumber == 0 && character != 'I') || (characterNumber == 1 && character != 'M') || (characterNumber == 2 && character != 'P') || (characterNumber == 3 && character != 'S')) {
			return;
		}

		if (characterNumber > 44) {
			putc('\n', ofp);
			return;
		}

		if ((characterNumber > 3 && characterNumber < 16) || (characterNumber > 19)) {
			if (character == '\0') {
				putc(' ', ofp);
			} else {
				putc(character, ofp);
			}
		} else if (characterNumber == 16) {
				putc(' ', ofp);
		}

		characterNumber++;
	}

	return;
}

int main(int argc, char *argv[]) {
	FILE *fp;
	void filecopy(FILE *, FILE *);

	if (argc == 1) {
		describeSample(stdin, stdout);
	} else {
		while (--argc > 0) {
			fp = fopen(*++argv, "r");

			if (fp == NULL) {
				continue;
			}

			describeSample(fp, stdout);
			fclose(fp);
		}
	}

	return 0;
}
