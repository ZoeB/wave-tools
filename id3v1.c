/* ID3v1 tag viewer, by Zoe Blade */

/* See http://id3.org/ID3v1 for the spec */

#include <stdio.h>

char title[30] = "                              ";
char artist[30] = "                              ";
char album[30] = "                              ";
char year[4] = "    ";
char comment[30] = "                              ";
char genre[1] = " ";

void describeFile(FILE *inputFilePointer, FILE *outputFilePointer) {
	fseek(inputFilePointer, -128, SEEK_END);

	/* If the last 128 chars don't begin with "TAG", they're not an
	   ID3v1 tag.  Quit. */

	if (getc(inputFilePointer) != 'T') {
		printf("No ID3v1 tag found.\n\n");
		return;
	}

	if (getc(inputFilePointer) != 'A') {
		printf("No ID3v1 tag found.\n\n");
		return;
	}

	if (getc(inputFilePointer) != 'G') {
		printf("No ID3v1 tag found.\n\n");
		return;
	}

	/* ID3v1 tag found */

	fread(title, 30, 1, inputFilePointer);
	fread(artist, 30, 1, inputFilePointer);
	fread(album, 30, 1, inputFilePointer);
	fread(year, 4, 1, inputFilePointer);
	fread(comment, 30, 1, inputFilePointer);
	fread(genre, 1, 1, inputFilePointer);

	printf("Title   : %s\n", title);
	printf("Artist  : %s\n", artist);
	printf("Album   : %s\n", album);
	printf("Year    : %s\n", year);
	printf("Comment : %s\n", comment);
	printf("Genre   : %s\n\n", genre);
	return;
}

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

			printf("%s\n", *argv);
			describeFile(filePointer, stdout);
			fclose(filePointer);
		}
	}

	return 0;
}
