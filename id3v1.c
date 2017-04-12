/* ID3v1 tag viewer, by Zoe Blade */

/* See http://id3.org/ID3v1 for the spec */

#include <stdio.h>

char title[30] = "                              ";
char artist[30] = "                              ";
char album[30] = "                              ";
char year[4] = "    ";
char comment[30] = "                              ";
char genre = '\0';
const char *genres[148];

void describeFile(FILE *inputFilePointer, FILE *outputFilePointer) {
	fseek(inputFilePointer, -128, SEEK_END);

	/* If the last 128 chars don't begin with "TAG", they're not an
	   ID3v1 tag.  Quit. */

	if (getc(inputFilePointer) != 'T' || getc(inputFilePointer) != 'A' || getc(inputFilePointer) != 'G') {
		printf("No ID3v1 tag found.\n\n");
		return;
	}

	/* ID3v1 tag found */

	fread(title, 30, 1, inputFilePointer);
	fread(artist, 30, 1, inputFilePointer);
	fread(album, 30, 1, inputFilePointer);
	fread(year, 4, 1, inputFilePointer);
	fread(comment, 30, 1, inputFilePointer);
	genre = getc(inputFilePointer);

	printf("Title   : %s\n", title);
	printf("Artist  : %s\n", artist);
	printf("Album   : %s\n", album);
	printf("Year    : %s\n", year);
	printf("Comment : %s\n", comment);

	if (comment[28] == '\0' && comment[29] != '\0') {
		/* The tag is ID3v1.1 */
		printf("Track   : %u\n", comment[29]);
	}

	printf("Genre   : %s\n\n", genres[genre]);

	return;
}

int main(int argc, char *argv[]) {
	FILE *filePointer;

	/* See "lame --genre-list" */
	genres[0] = "Blues";
	genres[1] = "Classic Rock";
	genres[2] = "Country";
	genres[3] = "Dance";
	genres[4] = "Disco";
	genres[5] = "Funk";
	genres[6] = "Grunge";
	genres[7] = "Hip-Hop";
	genres[8] = "Jazz";
	genres[9] = "Metal";
	genres[10] = "New Age";
	genres[11] = "Oldies";
	genres[12] = "Other";
	genres[13] = "Pop";
	genres[14] = "R&B";
	genres[15] = "Rap";
	genres[16] = "Reggae";
	genres[17] = "Rock";
	genres[18] = "Techno";
	genres[19] = "Industrial";
	genres[20] = "Alternative";
	genres[21] = "Ska";
	genres[22] = "Death Metal";
	genres[23] = "Pranks";
	genres[24] = "Soundtrack";
	genres[25] = "Euro-Techno";
	genres[26] = "Ambient";
	genres[27] = "Trip-Hop";
	genres[28] = "Vocal";
	genres[29] = "Jazz+Funk";
	genres[30] = "Fusion";
	genres[31] = "Trance";
	genres[32] = "Classical";
	genres[33] = "Instrumental";
	genres[34] = "Acid";
	genres[35] = "House";
	genres[36] = "Game";
	genres[37] = "Sound Clip";
	genres[38] = "Gospel";
	genres[39] = "Noise";
	genres[40] = "Alternative Rock";
	genres[41] = "Bass";
	genres[42] = "Soul";
	genres[43] = "Punk";
	genres[44] = "Space";
	genres[45] = "Meditative";
	genres[46] = "Instrumental Pop";
	genres[47] = "Instrumental Rock";
	genres[48] = "Ethnic";
	genres[49] = "Gothic";
	genres[50] = "Darkwave";
	genres[51] = "Techno-Industrial";
	genres[52] = "Electronic";
	genres[53] = "Pop-Folk";
	genres[54] = "Eurodance";
	genres[55] = "Dream";
	genres[56] = "Southern Rock";
	genres[57] = "Comedy";
	genres[58] = "Cult";
	genres[59] = "Gangsta";
	genres[60] = "Top 40";
	genres[61] = "Christian Rap";
	genres[62] = "Pop/Funk";
	genres[63] = "Jungle";
	genres[64] = "Native US";
	genres[65] = "Cabaret";
	genres[66] = "New Wave";
	genres[67] = "Psychedelic";
	genres[68] = "Rave";
	genres[69] = "Showtunes";
	genres[70] = "Trailer";
	genres[71] = "Lo-Fi";
	genres[72] = "Tribal";
	genres[73] = "Acid Punk";
	genres[74] = "Acid Jazz";
	genres[75] = "Polka";
	genres[76] = "Retro";
	genres[77] = "Musical";
	genres[78] = "Rock & Roll";
	genres[79] = "Hard Rock";
	genres[80] = "Folk";
	genres[81] = "Folk-Rock";
	genres[82] = "National Folk";
	genres[83] = "Swing";
	genres[84] = "Fast Fusion";
	genres[85] = "Bebob";
	genres[86] = "Latin";
	genres[87] = "Revival";
	genres[88] = "Celtic";
	genres[89] = "Bluegrass";
	genres[90] = "Avantgarde";
	genres[91] = "Gothic Rock";
	genres[92] = "Progressive Rock";
	genres[93] = "Psychedelic Rock";
	genres[94] = "Symphonic Rock";
	genres[95] = "Slow Rock";
	genres[96] = "Big Band";
	genres[97] = "Chorus";
	genres[98] = "Easy Listening";
	genres[99] = "Acoustic";
	genres[100] = "Humour";
	genres[101] = "Speech";
	genres[102] = "Chanson";
	genres[103] = "Opera";
	genres[104] = "Chamber Music";
	genres[105] = "Sonata";
	genres[106] = "Symphony";
	genres[107] = "Booty Bass";
	genres[108] = "Primus";
	genres[109] = "Porn Groove";
	genres[110] = "Satire";
	genres[111] = "Slow Jam";
	genres[112] = "Club";
	genres[113] = "Tango";
	genres[114] = "Samba";
	genres[115] = "Folklore";
	genres[116] = "Ballad";
	genres[117] = "Power Ballad";
	genres[118] = "Rhythmic Soul";
	genres[119] = "Freestyle";
	genres[120] = "Duet";
	genres[121] = "Punk Rock";
	genres[122] = "Drum Solo";
	genres[123] = "A Cappella";
	genres[124] = "Euro-House";
	genres[125] = "Dance Hall";
	genres[126] = "Goa";
	genres[127] = "Drum & Bass";
	genres[128] = "Club-House";
	genres[129] = "Hardcore";
	genres[130] = "Terror";
	genres[131] = "Indie";
	genres[132] = "BritPop";
	genres[133] = "Negerpunk";
	genres[134] = "Polsk Punk";
	genres[135] = "Beat";
	genres[136] = "Christian Gangsta";
	genres[137] = "Heavy Metal";
	genres[138] = "Black Metal";
	genres[139] = "Crossover";
	genres[140] = "Contemporary Christian";
	genres[141] = "Christian Rock";
	genres[142] = "Merengue";
	genres[143] = "Salsa";
	genres[144] = "Thrash Metal";
	genres[145] = "Anime";
	genres[146] = "JPop";
	genres[147] = "SynthPop";

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
