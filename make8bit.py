# Wavesplit
# For Python 3
# By Zoe Blade

# Converts 16-bit and 24-bit .wav files into 8-bit .wav files

import glob # For command line wildcards
import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
inputFilenames = []

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.wav'):
		filenames = glob.glob(argument)

		for filename in filenames:
			inputFilenames.append(filename)

		continue

if (len(inputFilenames) == 0):
	print("""\
Usage:
python3 make8bit.py input.wav
	""")
	exit()

# Cycle through files
for inputFilename in inputFilenames:
	outputFilename = inputFilename[:-4] + '-8bit' + '.wav'

	try:
		inputFile = wave.open(inputFilename, 'r')
	except:
		print(inputFilename, "doesn't look like a valid .wav file.  Skipping.")
		continue

	try:
		outputFile = wave.open(outputFilename, 'w')
		outputFile.setnchannels(inputFile.getnchannels())
		outputFile.setsampwidth(1)
		outputFile.setframerate(inputFile.getframerate())
	except:
		print("I couldn't write to", outputFilename, "Skipping.")
		continue

	numberOfChannels = inputFile.getnchannels()
	sampleWidth = inputFile.getsampwidth()

	if (sampleWidth != 2 and sampleWidth != 3):
		print(inputFilename, "is neither 16-bit nor 24-bit.  Skipping.")
		continue

	print('Converting', inputFilename, 'into', outputFilename)

	for iteration in range(0, inputFile.getnframes()):
		allChannelsAsBinary = inputFile.readframes(1)

		for channelNumber in range (numberOfChannels):
			channelNumber = channelNumber + 1
			channelStart = (channelNumber - 1) * sampleWidth
			channelEnd = channelNumber * sampleWidth

			# Ignore all but the most significant byte
			if (sampleWidth == 3):
				channelAsInteger = struct.unpack('<3b', allChannelsAsBinary[channelStart:channelEnd])
				channelAsInteger = int(channelAsInteger[2])
			else: # It's 2
				channelAsInteger = struct.unpack('<2b', allChannelsAsBinary[channelStart:channelEnd])
				channelAsInteger = int(channelAsInteger[1])

			channelAsBinary = struct.pack('<B', channelAsInteger + 128)
			outputFile.writeframes(channelAsBinary)

	inputFile.close()
	outputFile.close()
	print(inputFilename, "finished converting")
