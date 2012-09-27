# Wavesplit
# For Python 3
# By Zoe Blade

# Splits up a big .wav file into several smaller .wav files, one per sound

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
	if (argument[-4:].lower() == '.wav'):
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

Options: (may appear before or after arguments)
	--threshold=foo
		set the cutoff point between signal and noise (default is 1024, any number between 1 and 32767 is valid)
	--duration=foo
		require this many consecutive samples below the cutoff point in order to close the output file (default is 11025, a quarter of a second at CD quality)
	""")
	exit()

outputFilenamePrefix = inputFilename[:-4]
outputFilenameNumber = 0

try:
	inputFile = wave.open(inputFilename, 'r')
	framerate = inputFile.getframerate()
	numberOfChannels = inputFile.getnchannels()
	sampleWidth = inputFile.getsampwidth()
except:
	print('Please specify a valid .wav file')
	exit()

currentlyWriting = False
allChannelsBeneathThreshold = 0

for iteration in range(0, inputFile.getnframes()):
	allChannelsAsBinary = inputFile.readframes(1)
	allChannelsCurrentlyBeneathThreshold = True

	for channelNumber in range (numberOfChannels):
		channelNumber = channelNumber + 1
		channelStart = (channelNumber - 1) * sampleWidth
		channelEnd = channelNumber * sampleWidth
		channelAsInteger = struct.unpack('<h', allChannelsAsBinary[channelStart:channelEnd])
		channelAsInteger = channelAsInteger[0]

		if (channelAsInteger < 0):
			channelAsInteger = 0 - channelAsInteger # Make readout unipolar

		if (channelAsInteger >= threshold):
			allChannelsCurrentlyBeneathThreshold = False

	if (currentlyWriting == True):
		# We are currently writing
		outputFile.writeframes(allChannelsAsBinary)

		if (allChannelsCurrentlyBeneathThreshold == True):
			allChannelsBeneathThresholdDuration = allChannelsBeneathThresholdDuration + 1

			if (allChannelsBeneathThresholdDuration >= duration):
				currentlyWriting = False
				outputFile.close()
		else:
				allChannelsBeneathThresholdDuration = 0
	else:
		# We're not currently writing
		if (allChannelsCurrentlyBeneathThreshold == False):
			currentlyWriting = True
			allChannelsBeneathThresholdDuration = 0
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
