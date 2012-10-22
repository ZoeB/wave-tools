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
		data.append(b'\x3F') # TODO: Check what to make this so the speaker's centered.  127?  128?  0?  255?

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

	# Write the sample frequency.  I'm not entirely sure what the (German) spec is saying, but it looks like this might perhaps be divided by 5, as it looks like "200 nSek" (miliseconds?) are somehow involved.  So let's try that!
	sampleFrequency = inputFile.getframerate()
	sampleFrequency = int(sampleFrequency / 5)
	sampleFrequencyByte1 = sampleFrequency >> 9 & 127 # I'm going to guess the most significant byte goes first, but it's just a guess.
	sampleFrequencyByte2 = sampleFrequency >> 1 & 127
	sampleFrequencyByte3 = (sampleFrequency >> 7 & 3) & (sampleFrequency & 1) # It's late and this may be stupid.  I'm trying to take a (presumably 16 bit) sample frequency and only keep the eighth and sixteenth bits, in places fifteen and sixteen (counting from left to right).
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
			byteatumAsBinary = struct.pack('B', byte)
			outputFile.write(bytes(byteatumAsBinary))

	# Output last byte, even though it's not full
	byteatumAsBinary = struct.pack('B', byte)
	outputFile.write(bytes(byteatumAsBinary))

	# Output sysex footer: F7 = end sysex dump
	outputFile.write(b'\xF7')

	inputFile.close()
	outputFile.close()

	print(inputFilename, "converted to", outputFilename)
