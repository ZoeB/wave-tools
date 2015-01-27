# Normalise
# For Python 3
# By Zoe Blade

# Makes .wav files as loud as they can be

import os # For renaming the output files over the top of the input files
import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
delete = False
inputFilenames = []

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.wav'):
		inputFilenames.append(argument)
		continue

	# Replace original files
	if (argument == '-d'):
		delete = True

if (len(inputFilenames) == 0):
	print("""\
Usage:
python3 normalise.py [option...] input.wav

Options: (may appear before or after arguments)
	-d
		replace original files
	""")
	exit()

# Cycle through files
for inputFilename in inputFilenames:
	outputFilename = inputFilename[:-4] + '-loud' + '.wav'

	try:
		inputFile = wave.open(inputFilename, 'r')
	except:
		print(inputFilename, "doesn't look like a valid .wav file.  Skipping.")
		continue

	numberOfChannels = inputFile.getnchannels()
	sampleWidth = inputFile.getsampwidth()

	try:
		outputFile = wave.open(outputFilename, 'w')
		outputFile.setnchannels(numberOfChannels)
		outputFile.setsampwidth(sampleWidth)
		outputFile.setframerate(inputFile.getframerate())
	except:
		print("I couldn't write to", outputFilename, "Skipping.")
		continue

	# Read
	print('Analysing', inputFilename)
	peak = 0

	for iteration in range(0, inputFile.getnframes()):
		allChannelsAsBinary = inputFile.readframes(1)

		for channelNumber in range (numberOfChannels):
			channelNumber = channelNumber + 1
			channelStart = (channelNumber - 1) * sampleWidth
			channelEnd = channelNumber * sampleWidth
			channelAsInteger = struct.unpack('<h', allChannelsAsBinary[channelStart:channelEnd])
			channelAsInteger = channelAsInteger[0]

			if (channelAsInteger < 0):
				channelAsInteger = 0 - channelAsInteger # Make readout unipolar

			if (channelAsInteger > peak):
				peak = channelAsInteger

	inputFile.rewind()
	print("Peak: ", peak, "out of 32767")

	# Write
	if (delete == True):
		print('Normalising', inputFilename)
	else:
		print('Normalising', inputFilename, 'into', outputFilename)

	for iteration in range(0, inputFile.getnframes()):
		allChannelsAsBinary = inputFile.readframes(1)
		allChannelsAsIntegers = []

		for channelNumber in range (numberOfChannels):
			channelNumber = channelNumber + 1
			channelStart = (channelNumber - 1) * sampleWidth
			channelEnd = channelNumber * sampleWidth
			channelAsInteger = struct.unpack('<h', allChannelsAsBinary[channelStart:channelEnd])
			channelAsInteger = channelAsInteger[0]
			channelAsInteger = round(channelAsInteger / peak * 32767) # Increase the volume
			allChannelsAsIntegers.append(channelAsInteger)

		allChannelsAsBinary = struct.pack('<h', *allChannelsAsIntegers)
		outputFile.writeframes(allChannelsAsBinary)

	inputFile.close()
	outputFile.close()

	if (delete == True):
		os.rename(outputFilename, inputFilename)
		print(inputFilename, "overwritten")
	else:
		print(inputFilename, "converted to", outputFilename)
