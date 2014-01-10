/* Impulse Tracker file lister, by Zoe Blade */

/* TODO: If no arguments are supplied, list all files in the present working directory */

#include <stdio.h>
#include "itls.h"

void describeFile(FILE *inputFilePointer, FILE *outputFilePointer) {
	while (1) {
		/* If the input doesn't begin with "IMP", it's not a block of
		   Impulse Tracker data.  Quit. */

		if (getc(inputFilePointer) != 'I')
			return;

		if (getc(inputFilePointer) != 'M')
			return;

		if (getc(inputFilePointer) != 'P')
			return;

		switch (getc(inputFilePointer)) {
		case 'I': /* Instrument */
			describeInstrument(inputFilePointer, outputFilePointer);
			break;

		case 'M': /* Module (song) */
			describeModule(inputFilePointer, outputFilePointer);
			break;

		case 'S': /* Sample */
			describeSample(inputFilePointer, outputFilePointer);
			break;

		default:
			return;
		}
	}
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
	   and instrument name.  Skip to the end of the instrument data block,
	   print a newline and return.  There are 554 bytes per instrument,
	   minus the 31 we've already read so far, so skip ahead 523 bytes. */

	fseek(inputFilePointer, 497, SEEK_CUR); /* TODO: Work out why 497 seems to work better than 523.  I reached this number using trial and error, which is not a good sign. */
	putc('\n', outputFilePointer);
	return;
}

void describeModule(FILE *inputFilePointer, FILE *outputFilePointer) {
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

	/* We've finished successfully printing out a module's filename and
	   module name.  Skip to the end of the module data block, print a
	   newline and return. */

	/* TODO: This!  It's trickier for the module header, as it's a
	   variable length. */

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

	/* We've finished successfully printing out a sample's filename and
	   sample name.  Skip to the end of the sample data block, print a
	   newline and return.  There are 80 bytes per sample, minus the 19
	   we've already read so far, so skip ahead 61 bytes. */

	fseek(inputFilePointer, 35, SEEK_CUR); /* TODO: Work out why 35 seems to work better than 80.  I reached this number using trial and error, which is not a good sign. */
	putc('\n', outputFilePointer);
	return;
}

/* This is mostly ripping off K&R's ANSI C, page 162, "Cat". */

int main(int argc, char *argv[]) {
	FILE *filePointer;

	if (argc == 1) {
		return 0; /* Only work with named files, not stdin */
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
