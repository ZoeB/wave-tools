/* Impulse Tracker sample describer, by Zoe Blade */

/* This is mostly ripping off ANSI C page 162, Cat */

#include <stdio.h>

void describeSample(FILE *ifp, FILE *ofp) {
	int characterNumber = 0;
	int character;

	/* TODO: Fix redundancy in checking if limit's reached */
	while (characterNumber < 72) {
		character = getc(ifp);

		if (character == EOF || characterNumber == 72) {
			return;
		}

		putc(character, ofp);
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
