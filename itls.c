/* Impulse Tracker file lister, by Zoe Blade */

#include <stdio.h>
#include "itls.h"

void describeFile(FILE *inputFilePointer, FILE *outputFilePointer) {
	int char1 = '\0';
	int char2 = '\0';
	int char3 = '\0';
	int char4 = '\0';

	/*
	 * Every interesting block starts with the characters "IMP".
	 *
	 * Not knowing where they should start means reading everything
	 * indiscriminately, which is sloppy coding on my part and liable to
	 * be slow and possibly come up with false positives, but then again
	 * it's thorough and will allow whole concatenated gobs of Impulse
	 * Tracker data to be sent to the program even via stdin.  Most
	 * significantly for me, it means I get to re-use the instrument and
	 * sample detecting routines from within module and instrument data.
	 * Nevertheless, I should rewrite this recursion at some point.  For
	 * one thing, it would be nice if recursed data is indicated with a
	 * lower case "i" or "s" to differentiate it in the output stream.
	 */

	while (char4 != EOF) {
		char1 = char2;
		char2 = char3;
		char3 = char4;
		char4 = getc(inputFilePointer);

		if (char1 != 'I' || char2 != 'M' || char3 != 'P') {
			continue;
		}

		switch (char4) {
		case 'I': /* Instrument */
			describeInstrument(inputFilePointer, outputFilePointer);
			break;

		case 'M': /* Module (song) */
			describeModule(inputFilePointer, outputFilePointer);
			break;

		case 'S': /* Sample */
			describeSample(inputFilePointer, outputFilePointer);
			break;
		}

	}

	return;
}

void describeInstrument(FILE *inputFilePointer, FILE *outputFilePointer) {
	/* TODO: name its samples too, one S-line each */
	int characterNumber;
	int character;

	putc('I', outputFilePointer);
	putc(' ', outputFilePointer);

	for (characterNumber = 4; characterNumber < 57; characterNumber++) {
		character = getc(inputFilePointer);

		if (character == EOF) {
			return;
		}

		if ((characterNumber > 3 && characterNumber < 16) || (characterNumber > 31)) {
			/* Only print out the filename and instrument name, nothing in between. */
			if (character == '\0') {
				/* Pad filenames and instrument names with spaces, not NULLs. */
				putc(' ', outputFilePointer);
			} else {
				putc(character, outputFilePointer);
			}
		} else if (characterNumber == 16) {
				/* Print a gap between the filename and instrument name. */
				putc(' ', outputFilePointer);
		}
	}

	/* We've finished successfully printing out an instrument's filename
	   and instrument name.  Print a newline and return. */

	putc('\n', outputFilePointer);
	return;
}

void describeModule(FILE *inputFilePointer, FILE *outputFilePointer) {
	/* TODO: name its instruments and samples too, one I- and S-line each */
	int characterNumber;
	int character;
	int i;

	putc('M', outputFilePointer);

	for (i = 0; i < 14; i++) {
		putc(' ', outputFilePointer); /* Modules have no internally
		                                 stored filenames */
	}

	for (characterNumber = 4; characterNumber < 30; characterNumber++) {
		character = getc(inputFilePointer);

		if (character == EOF) {
			return;
		}

		if (character == '\0') {
			/* Pad module names with spaces, not NULLs. */
			putc(' ', outputFilePointer);
		} else {
			putc(character, outputFilePointer);
		}
	}

	/* We've finished successfully printing out a sample's filename
	   and sample name.  Print a newline and return. */

	putc('\n', outputFilePointer);
	return;
}

void describeSample(FILE *inputFilePointer, FILE *outputFilePointer) {
	int characterNumber;
	int character;

	putc('S', outputFilePointer);
	putc(' ', outputFilePointer);

	for (characterNumber = 4; characterNumber < 45; characterNumber++) {
		character = getc(inputFilePointer);

		if (character == EOF) {
			return;
		}

		if ((characterNumber > 3 && characterNumber < 16) || (characterNumber > 19)) {
			/* Only print out the filename and sample name, nothing in between. */
			if (character == '\0') {
				/* Pad filenames and sample names with spaces, not NULLs. */
				putc(' ', outputFilePointer);
			} else {
				putc(character, outputFilePointer);
			}
		} else if (characterNumber == 16) {
				/* Print a gap between the filename and sample name. */
				putc(' ', outputFilePointer);
		}
	}

	/* We've finished successfully printing out a sample's filename
	   and sample name.  Print a newline and return. */

	putc('\n', outputFilePointer);
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
