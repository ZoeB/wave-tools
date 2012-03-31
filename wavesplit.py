# Wavesplit version 1, for Python 3.  By ZoëB, 2012-03-31.

# This splits up a mono .wav file into several smaller .wav files,
# one per sound, leaving out the gaps.

import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Make sure the user has specified exactly three arguments...
if (len(sys.argv) != 4):
	print('Please specify a threshold, duration, and single .wav file')
	print('For example: python3 wavesplit.py 1000 1000 input.wav')
	exit()

# ...and that the last argument is a .wav file.
threshold = int(sys.argv[1])
duration = int(sys.argv[2])
inputFilename = sys.argv[3]

if (inputFilename[-4:] != '.wav'):
	print('Please specify a .wav file')
	exit()

outputFilenamePrefix = inputFilename[:-4]
outputFilenameNumber = 0

try:
	inputFile = wave.open(inputFilename, 'r')
	samplewidth = inputFile.getsampwidth()
	framerate = inputFile.getframerate()
except:
	print('Please specify a valid .wav file')
	exit()

if (inputFile.getnchannels() != 1):
	print('Please specify a mono .wav file') # It should be trivial to support stereo files too, but let's not get ahead of ourselves here.
	exit()

currentlyWriting = False
samplesBeneathThreshold = 0

for iteration in range(0, inputFile.getnframes()):
	sample = inputFile.readframes(1)

	sampleInteger = struct.unpack('<h', sample)
	sampleInteger = sampleInteger[0]

	if (sampleInteger < 0):
		sampleInteger = 0 - sampleInteger # Unipolar!

	if (currentlyWriting == True):
		# We are currently writing
		outputFile.writeframes(sample)

		if (sampleInteger < threshold):
			samplesBeneathThreshold = samplesBeneathThreshold + 1

			if (samplesBeneathThreshold >= duration):
				currentlyWriting = False
				outputFile.close()
		else:
			samplesBeneathThreshold = 0
	else:
		# We're not currently writing
		if (sampleInteger >= threshold):
			currentlyWriting = True
			samplesBeneathThreshold = 0
			outputFilenameNumber = outputFilenameNumber + 1
			outputFilename = str(outputFilenameNumber)
			outputFilename = outputFilename.zfill(2) # Pad to 2 digits
			outputFilename = outputFilenamePrefix + '-' + outputFilename + '.wav'
			print('Writing to', outputFilename)
			outputFile = wave.open(outputFilename, 'w')
			outputFile.setnchannels(inputFile.getnchannels())
			outputFile.setsampwidth(inputFile.getsampwidth())
			outputFile.setframerate(inputFile.getframerate())

if (currentlyWriting == True):
	outputFile.close()
