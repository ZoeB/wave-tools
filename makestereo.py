# Makestereo
# For Python 3
# By Zoe Blade

# Converts mono .wav files into stereo .wav files

import sys # For command line arguments
import wave # For .wav input and output

# Set sensible defaults
inputFilenames = []

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.wav'):
		inputFilenames.append(argument)
		continue

if (len(inputFilenames) == 0):
	print("""\
Usage:
python3 makestereo.py [option...] input.wav
	""")
	exit()

# Cycle through files
for inputFilename in inputFilenames:
	outputFilename = inputFilename[:-4] + '-stereo' + '.wav'

	try:
		inputFile = wave.open(inputFilename, 'r')
	except:
		print(inputFilename, "doesn't look like a valid .wav file.  Skipping.")
		continue

	if (inputFile.getnchannels() != 1):
		print(inputFilename, "isn't mono.  Skipping.")
		continue

	try:
		outputFile = wave.open(outputFilename, 'w')
		outputFile.setnchannels(2)
		outputFile.setsampwidth(inputFile.getsampwidth())
		outputFile.setframerate(inputFile.getframerate())
	except:
		print("I couldn't write to", outputFilename, "Skipping.")
		continue

	sampleWidth = inputFile.getsampwidth()

	for iteration in range (0, inputFile.getnframes()):
		datum = inputFile.readframes(1)
		outputFile.writeframes(datum)
		outputFile.writeframes(datum)

	inputFile.close()
	outputFile.close()

	print(inputFilename, "converted to", outputFilename)
