# MCV24sysextobin
# For Python 3
# By Zoe Blade

# Converts MCV-24 sysex dumps into binary

import struct # For converting the binary data to integers
import sys # For command line arguments

# Set sensible defaults
inputFilenames = []

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.syx'):
		inputFilenames.append(argument)
		continue

if (len(inputFilenames) == 0):
	print("""\
Usage:
python3 mcv24sysextobin.py input.syx
	""")
	exit()

# Cycle through files
for inputFilename in inputFilenames:
	outputFilename = inputFilename[:-4] + '.bin'

	try:
		inputFile = open(inputFilename, 'rb').read() # It will all fit in memory
	except:
		print(inputFilename, "doesn't look like a valid .syx file.  Skipping.")
		continue

	try:
		outputFile = open(outputFilename, 'wb')
	except:
		print("I couldn't write to", outputFilename, "Skipping.")
		continue

	# Do magic
	byteNumber = 0
	finished = False

	for inputByte in inputFile:
		if (finished == True):
			continue

		# Ignore the first 8 bytes (1 for "Sysex start", 3 for "Doepfer", 4 I'm not sure about, but the first of them probably means "MCV-24 patch")
		if (byteNumber < 8):
			byteNumber = byteNumber + 1
			continue

		# Ignore the "Sysex end" byte
		if (inputByte == 247): # 247 == xF7
			finished = True
			continue

		# Pair up the bytes
		if (byteNumber & 1 == False):
			outputByte = inputByte * 128
		else:
			outputByte = outputByte + inputByte
			outputFile.write(bytes(struct.pack('B', outputByte)))

		byteNumber = byteNumber + 1

	outputFile.close()

	print(inputFilename, "converted to", outputFilename)
