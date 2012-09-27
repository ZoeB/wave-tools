# Makemono
# For Python 3
# By Zoe Blade

# Converts stereo .wav files into mono .wav files

import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
channel = 'both'
inputFilename = ''

acceptableChannels = ['both', 'left', 'right']

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.wav'):
		inputFilename = argument
		continue

	# Override the channel
	if (argument[:10] == '--channel='):
		if (argument[10:] in acceptableChannels):
			channel = argument[10:]
			continue
		else:
			print(argument[10:], "ain't any channel I ever heard of")
			exit()

if (inputFilename == ''):
	print("""\
Usage:
python3 makemono.py [option...] input.wav

Options: (may appear before or after arguments)
	--channel=foo
		set which channel to extract (default is both, other options are left and right)
	""")
	exit()

outputFilename = inputFilename[:-4] + '-mono' + '.wav'

try:
	inputFile = wave.open(inputFilename, 'r')
	outputFile = wave.open(outputFilename, 'w')
	outputFile.setnchannels(1)
	outputFile.setsampwidth(inputFile.getsampwidth())
	outputFile.setframerate(inputFile.getframerate())
except:
	print('Please specify a valid .wav file')
	exit()

if (inputFile.getnchannels() != 2):
	print('Please specify a stereo .wav file')
	exit()

sampleWidth = inputFile.getsampwidth()

if (channel == 'both'):
	print('Extracting both channels of', inputFilename, 'into', outputFilename)
elif (channel == 'left'):
	print('Extracting left channel of', inputFilename, 'into', outputFilename)
elif (channel == 'right'):
	print('Extracting right channel of', inputFilename, 'into', outputFilename)

for iteration in range (0, inputFile.getnframes()):
	datum = inputFile.readframes(1)

	if (channel == 'both'):
		leftChannelAsInteger = struct.unpack('<h', datum[:sampleWidth])
		leftChannelAsInteger = leftChannelAsInteger[0]
		rightChannelAsInteger = struct.unpack('<h', datum[sampleWidth:])
		rightChannelAsInteger = rightChannelAsInteger[0]
		combinationAsInteger = (leftChannelAsInteger + rightChannelAsInteger) / 2
		combinationAsInteger = int(combinationAsInteger)
		combinationAsBinary = struct.pack('<h', combinationAsInteger)
		outputFile.writeframes(combinationAsBinary)
	elif (channel == 'left'):
		outputFile.writeframes(datum[:sampleWidth]) # Write the left channel; ignore the right channel.
	elif (channel == 'right'):
		outputFile.writeframes(datum[sampleWidth:]) # Write the right channel; ignore the left channel.

inputFile.close()
outputFile.close()

print('Extraction complete')
exit()
