# Makemono, version 2, for Python 3.
# By ZoëB, 2012-03-31 to 2012-04-01.

# This converts a stereo .wav file to mono.
# It's useful if, for instance, you've recorded a synthesiser using a
# stereo only sound recorder.

import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
channel = 'left'
inputFilename = ''

acceptableChannels = {'left', 'right'}

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:] == '.wav'):
		inputFilename = argument
		continue

	# Override the channel
	if (argument[:10] == '--channel=' and argument[10:] in acceptableChannels):
		channel = argument[10:]
		continue

if (inputFilename == ''):
	print("""\
Usage:
python3 makemono.py [option...] input.wav

Options: (may appear before or after arguments)
	--channel=foo
		set which channel to extract (default is left, other option is right)
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

if (channel == 'left'):
	print('Extracting left channel of', inputFilename, 'into', outputFilename)
elif (channel == 'right'):
	print('Extracting right channel of', inputFilename, 'into', outputFilename)

for iteration in range (0, inputFile.getnframes()):
	datum = inputFile.readframes(1)

	if (channel == 'left'):
		outputFile.writeframes(datum[:sampleWidth]) # Write the left channel; ignore the right channel.
	elif (channel == 'right'):
		outputFile.writeframes(datum[sampleWidth:]) # Write the right channel; ignore the left channel.

inputFile.close()
outputFile.close()

print('Extraction complete')
exit()
