# Makedoepfer
# For Python 3
# By Zoe Blade

# Converts mono 8-bit .wav files into Doepfer A-112 sysex dump files

import struct # For converting the binary data to integers
import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
bank = 1
inputFilenames = []

acceptableBanks = [1, 2]

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.wav'):
		inputFilenames.append(argument)
		continue

	# Override the bank
	if (argument[:7] == '--bank='):
		if (int(argument[7:]) in acceptableBanks):
			bank = int(argument[7:])
			continue
		else:
			print(argument[7:], "ain't any bank I ever heard of")
			exit()

if (len(inputFilenames) == 0):
	print("""\
Usage:
python3 makedoepfer.py [option...] input.wav

Options: (may appear before or after arguments)
	--bank=foo
		set which A-112 bank to write to (default is 1, other option is 2)
	""")
	exit()

# Cycle through files
for inputFilename in inputFilenames:
	outputFilename = inputFilename[:-4] + '.syx'

	try:
		inputFile = wave.open(inputFilename, 'r')
	except:
		print(inputFilename, "doesn't look like a valid .wav file.  Skipping.")
		continue

	if (inputFile.getnchannels() != 1):
		print(inputFilename, "isn't mono.  Skipping.")
		continue

	if (inputFile.getsampwidth() != 1):
		print(inputFilename, "isn't 8-bit.  Skipping.")
		continue

	try:
		outputFile = open(outputFilename, 'wb')
	except:
		print("I couldn't write to", outputFilename, "Skipping.")
		continue

	sampleWidth = inputFile.getsampwidth()

	data = []

	for iteration in range (0, inputFile.getnframes()):
		data.append(inputFile.readframes(1))

	# Truncate anything over 64k
	if (len(data) > 65536):
		del data[65536:]

	# Pad anything under 64k
	while (len(data) < 65536):
		data.append(b'\x80')

	# Write sysex header: F0 = start sysex dump; 00 20 20 = for Doepfer equipment; 7E = a sampledump for the A-112 module
	outputFile.write(b'\xF0')
	outputFile.write(b'\x00')
	outputFile.write(b'\x20')
	outputFile.write(b'\x20')
	outputFile.write(b'\x7E')

	if (bank == 1):
		outputFile.write(b'\x00')
	else: # bank == 2
		outputFile.write(b'\x01')

	# Write the sample frequency.  It looks like the A-112's clock cycle is once every 200 nanoseconds, in other words 5mHz, and it needs this to be divided by the sample frequency, so it knows how many cycles to pause for in between updating the output value.
	sampleFrequency = inputFile.getframerate()
	sampleFrequency = int(5000000 / sampleFrequency)
	sampleFrequencyByte1 = sampleFrequency >> 9 & 127 # I'm going to guess the most significant byte goes first, but it's just a guess.
	sampleFrequencyByte2 = sampleFrequency >> 1 & 127
	sampleFrequencyByte3 = (sampleFrequency >> 7 & 2) & (sampleFrequency & 1) # Take the 16 bit sample frequency and only keep the eighth and sixteenth bits, storing them in bits seven and eight (counting from left to right)
	outputFile.write(bytes(struct.pack('B', sampleFrequencyByte1)))
	outputFile.write(bytes(struct.pack('B', sampleFrequencyByte2)))
	outputFile.write(bytes(struct.pack('B', sampleFrequencyByte3)))

	# Write the 7 most significant bits of each 8-bit byte
	for datum in data:
		datumAsInteger = struct.unpack('B', datum)
		datumAsInteger = datumAsInteger[0]
		datumAsInteger = datumAsInteger >> 1
		datumAsBinary = struct.pack('B', datumAsInteger)
		outputFile.write(bytes(datumAsBinary))

	# Write the 1 least significant bit of each 8-bit byte, for 7 bytes at a time
	bitNumber = 0
	byte = 0

	for datum in data:
		datumAsInteger = struct.unpack('B', datum)
		datumAsInteger = datumAsInteger[0]
		datumAsInteger = datumAsInteger & 1
		datumAsInteger = datumAsInteger << bitNumber
		byte = byte | datumAsInteger
		bitNumber = bitNumber + 1

		if (bitNumber == 7):
			bitNumber = 0
			byteAsBinary = struct.pack('B', byte)
			outputFile.write(bytes(byteAsBinary))

	# Output last byte, even though it's not full
	byteAsBinary = struct.pack('B', byte)
	outputFile.write(bytes(byteAsBinary))

	# Output sysex footer: F7 = end sysex dump
	outputFile.write(b'\xF7')

	inputFile.close()
	outputFile.close()

	print(inputFilename, "converted to", outputFilename)
