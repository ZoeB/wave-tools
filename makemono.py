# Makemono, for Python 3.  By ZoëB, 2012-03-31 - 2012-03-31.

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

try:
	inputFile = wave.open(inputFilename, 'r')
except:
	print('Please specify a valid .wav file')
	exit()
else:
	print('Converting', inputFilename, 'to mono')
	exit()
