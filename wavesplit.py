# Wavesplit, version 2, for Python 3.
# By ZoëB, 2012-03-31 to 2012-04-01.

# This splits up a mono .wav file into several smaller .wav files,
# one per sound, leaving out the gaps.

import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
threshold = 1024 # This has to be a number between 1 and 32767
duration = 11025 # Measured in single samples
inputFilename = ''

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:] == '.wav'):
		inputFilename = argument
		continue

	# Override the threshold
	if (argument[:12] == '--threshold='):
		argument = int(argument[12:])

		if (argument > 0 and argument < 32768):
			threshold = argument
			continue
		else:
			print('The threshold must be an integer between 1 and 32767')
			exit()

	# Override the duration
	if (argument[:11] == '--duration='):
		argument = int(argument[11:])

		if (argument > 0):
			duration = argument
			continue
		else:
			print('The duration must be a positive integer')
			exit()

if (inputFilename == ''):
	print("""\
Usage:
python3 wavesplit.py [option...] input.wav
	""")
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
