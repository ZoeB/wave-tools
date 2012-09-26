# CD to Amiga
# For Python 3
# By Zoe Blade

# Converts 16-bit 44.1kHz .wav files into 8-bit 8363Hz .pcm files

import math # For floor
import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
inputFilenames = []

for argument in sys.argv:
	if (argument[-4:] == '.wav'):
		inputFilenames.append(argument)

if (len(inputFilenames) == 0):
	print("Please specify which .wav files you would like to convert.")
	exit()

# Make lookup table
whenToTakeASample = []
lastAmigaQualitySample = -1

for cdQualitySample in range(44100):
	currentAmigaQualitySample = math.floor(cdQualitySample / 44100 * 8363)

	if (currentAmigaQualitySample > lastAmigaQualitySample):
		whenToTakeASample.append(1)
		lastAmigaQualitySample = currentAmigaQualitySample
	else:
		whenToTakeASample.append(0)

# Cycle through files
for inputFilename in inputFilenames:
	outputFilename = inputFilename[:-4] + '.pcm'

	try:
		inputFile = wave.open(inputFilename, 'r')
		outputFile = open(outputFilename, 'wb')
	except:
		print(inputFilename, "doesn't look like a valid .wav file.  Skipping.")
		continue

	if (inputFile.getnchannels() != 1):
		print(inputFilename, "isn't mono.  Skipping.")
		continue

	if (inputFile.getsampwidth() != 2):
		print(inputFilename, "isn't 16-bit.  Skipping.")
		continue

	i = 0

	for iteration in range (0, inputFile.getnframes()):
		datumAsBinary = inputFile.readframes(1)

		i = i + 1

		if (i == 44100):
			i = 0

		if (whenToTakeASample[i] == 0):
			continue

		datumAsInteger = struct.unpack('<h', datumAsBinary)
		datumAsInteger = int(datumAsInteger[0])
		datumAsInteger = datumAsInteger >> 8 # Convert from 16-bit to 8-bit
		datumAsBinary = struct.pack('<B', datumAsInteger + 128)
		outputFile.write(datumAsBinary)

	inputFile.close()
	outputFile.close()
	print(inputFilename, "converted to", outputFilename)
