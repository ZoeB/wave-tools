# Makemono, for Python 3.  By ZoëB, 2012-03-31 - 2012-03-31.

import sys # For command line arguments
import wave # For .wav input and output

inputFilename = sys.argv[1]

if (len(sys.argv) != 2 or inputFilename[-4:] != '.wav'):
	print('Please specify a single .wav file')
	exit()

print('Converting', inputFilename, 'to mono')
exit()
