# Makestereo
# For Python 3
# By Zoe Blade

# Converts mono .wav files into stereo .wav files

import struct # For converting the (two's complement?) binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
inputFilename = ''

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:] == '.wav' or argument[-4:] == '.WAV'):
		inputFilename = argument
		continue

if (inputFilename == ''):
	print("""\
Usage:
python3 makestereo.py [option...] input.wav
	""")
	exit()

outputFilename = inputFilename[:-4] + '-stereo' + '.wav'

try:
	inputFile = wave.open(inputFilename, 'r')
	outputFile = wave.open(outputFilename, 'w')
	outputFile.setnchannels(2)
	outputFile.setsampwidth(inputFile.getsampwidth())
	outputFile.setframerate(inputFile.getframerate())
except:
	print('Please specify a valid .wav file')
	exit()

if (inputFile.getnchannels() != 1):
	print('Please specify a mono .wav file')
	exit()

sampleWidth = inputFile.getsampwidth()

for iteration in range (0, inputFile.getnframes()):
	datum = inputFile.readframes(1)
	outputFile.writeframes(datum)
	outputFile.writeframes(datum)

inputFile.close()
outputFile.close()

print('Duplication complete')
exit()
