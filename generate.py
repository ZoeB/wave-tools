# Generate
# For Python 3
# By Zoe Blade

# Uses additive synthesis to generate 8-bit .wav files, suitable for the Doepfer A-112

import math # For sine wave generation
import struct # For converting the integers to binary data
import sys # For command line arguments
import wave # For .wav output

# Set sensible defaults
mode = 'lowpass'
waveform = 'sawtooth'
outputFilenames = []

acceptableModes = ['highpass', 'lowpass']
acceptableWaveforms = ['sawtooth', 'square', 'triangle']

# Override the defaults
for argument in sys.argv:
	# Override the filename
	if (argument[-4:].lower() == '.wav'):
		outputFilenames.append(argument)
		continue

	# Override the mode
	if (argument[:7] == '--mode='):
		if (argument[7:] in acceptableModes):
			mode = argument[7:]
			continue
		else:
			print(argument[7:], "ain't any mode I ever heard of")
			exit()

	# Override the waveform type
	if (argument[:11] == '--waveform='):
		if (argument[11:] in acceptableWaveforms):
			waveform = argument[11:]
			continue
		else:
			print(argument[11:], "ain't any waveform I ever heard of")
			exit()

if (len(outputFilenames) == 0):
	print("""\
Usage:
python3 generate.py [option...] output.wav

Options: (may appear before or after arguments)
	--mode=foo
		set mode (default is lowpass, other option is highpass)
	--waveform=foo
		set which type of waveform to generate (default is sawtooth,
		other options are square and triangle)
	""")
	exit()

# Cycle through files
for outputFilename in outputFilenames:
	try:
		outputFile = wave.open(outputFilename, 'wb')
		outputFile.setnchannels(1) # Mono
		outputFile.setsampwidth(1) # 8-bit
		outputFile.setframerate(66976) # 261.626Hz for C-4 * 256 samples per cycle
	except:
		print("I couldn't write to", outputFilename, "Skipping.")
		continue

	# Make a sine wave lookup table
	sineWaveLookupTable = {frame: math.sin(frame / 256 * 2 * math.pi) * 127 for frame in range(256)}

	for maxHarmonic in range(1, 257): # Count from 1 to 256, not from 0 to 255
		for sample in range(256):
			wavestate = 0 # Start off in the middle

			if mode == 'highpass':
				for harmonic in range(maxHarmonic, 257):
					if (waveform == 'sawtooth'):
						wavestate = wavestate + (sineWaveLookupTable[sample * harmonic % 256] / harmonic)
					elif (waveform == 'square'):
						if (harmonic & 1):
							wavestate = wavestate + (sineWaveLookupTable[sample * harmonic % 256] / harmonic)
					elif (waveform == 'triangle'):
						if (harmonic & 3 == 3):
							wavestate = wavestate - (sineWaveLookupTable[sample * harmonic % 256] / harmonic ** 2)
						elif (harmonic & 1):
							wavestate = wavestate + (sineWaveLookupTable[sample * harmonic % 256] / harmonic ** 2)
			else: # Mode == lowpass
				for harmonic in range(1, maxHarmonic + 1):
					if (waveform == 'sawtooth'):
						wavestate = wavestate + (sineWaveLookupTable[sample * harmonic % 256] / harmonic)
					elif (waveform == 'square'):
						if (harmonic & 1):
							wavestate = wavestate + (sineWaveLookupTable[sample * harmonic % 256] / harmonic)
					elif (waveform == 'triangle'):
						if (harmonic & 3 == 3):
							wavestate = wavestate - (sineWaveLookupTable[sample * harmonic % 256] / harmonic ** 2)
						elif (harmonic & 1):
							wavestate = wavestate + (sineWaveLookupTable[sample * harmonic % 256] / harmonic ** 2)

			wavestate = int(wavestate / 1.85)
			wavestateAsBinary = struct.pack('B', wavestate + 128);
			outputFile.writeframes(wavestateAsBinary)

	outputFile.close()
	print("Generated", outputFilename)
