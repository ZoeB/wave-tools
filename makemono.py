# Makemono, for Python 3.  By ZoëB, 2012-03-31 - 2012-03-31.

# This converts a stereo .wav file to mono.
# It's useful if, for instance, you've recorded a synthesiser using a
# stereo only sound recorder.
# It works by simply disregarding the right channel entirely.

import sys # For command line arguments
import wave # For .wav input and output

# Make sure the user has specified exactly one argument...
if (len(sys.argv) != 2):
	print('Please specify a single .wav file')
	exit()

# ...and that argument is a .wav file.
inputFilename = sys.argv[1]

if (inputFilename[-4:] != '.wav'):
	print('Please specify a .wav file')
	exit()

outputFilename = inputFilename[:-4] + '-mono' + '.wav';

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

for iteration in range (0, inputFile.getnframes()):
	sample = inputFile.readframes(1)
	outputFile.writeframes(sample)

inputFile.close()
outputFile.close()
