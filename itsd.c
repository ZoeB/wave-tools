/* Impulse Tracker sample describer, by Zoe Blade */

#include <stdio.h>

void describeSample(FILE *ifp, FILE *ofp) {
	int characterNumber = 0;
	int character;

	while (1) {
		character = getc(ifp);

		if (character == EOF || (characterNumber == 0 && character != 'I') || (characterNumber == 1 && character != 'M') || (characterNumber == 2 && character != 'P') || (characterNumber == 3 && character != 'S')) {
			/* If the input is < 45 characters or doesn't begin with "IMPS",
			   it's not an Impulse Tracker sample.  Quit. */
			return;
		}

		if (characterNumber > 44) {
			/* We've finished successfully printing out a sample's filename
			   and sample name.  Print a newline and quit. */
			putc('\n', ofp);
			return;
		}

		if ((characterNumber > 3 && characterNumber < 16) || (characterNumber > 19)) {
			/* Only print out the filename and sample name, nothing in between. */
			if (character == '\0') {
				/* Pad filenames and sample names with spaces, not NULLs. */
				putc(' ', ofp);
			} else {
				putc(character, ofp);
			}
		} else if (characterNumber == 16) {
				/* Print a gap between the filename and sample name. */
				putc(' ', ofp);
		}

		characterNumber++;
	}

	return;
}

/* This is mostly ripping off K&R's ANSI C, page 162, "Cat". */

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
