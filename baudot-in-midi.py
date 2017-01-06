# ASCII to Baudot-in-MIDI
# For Python 2
# By Zoe Blade

# Converts a specified message to Baudot within a MIDI file, to embed messages in music as rhythmic harmonies

import midi # Installed from https://github.com/vishnubob/python-midi
import sys # For command line arguments

if len(sys.argv) < 2:
	print 'Please specify a message to convert'
	exit()

message = sys.argv[1].upper()
noteLength = 110

pattern = midi.Pattern()
track = midi.Track()
pattern.append(track)
tick = 0

for letter in message:
	if letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ':
		continue

	elements = [False, False, False, False, False]

	# Using https://en.wikipedia.org/wiki/Baudot_code#/media/File:International_Telegraph_Alphabet_2.jpg as a guide
	if letter in 'ABDEFJKQSUWXYZ':
		elements[0] = True

	if letter in 'ACGIJKLPQRUVW':
		elements[1] = True

	if letter in 'CFHIKMNPQSUVXY ':
		elements[2] = True

	if letter in 'BCDFGJKMNORVX':
		elements[3] = True

	if letter in 'BGHLMOPQTVWXYZ':
		elements[4] = True

	lineToPrint = letter + ' '
	elementCount = 0

	for element in elements:
		if element == True:
			lineToPrint += 'o'

			if elementCount == 0:
				track.append(midi.NoteOnEvent(tick=0, velocity=100, pitch=midi.E_4))
			elif elementCount == 1:
				track.append(midi.NoteOnEvent(tick=0, velocity=100, pitch=midi.C_4))
			elif elementCount == 2:
				track.append(midi.NoteOnEvent(tick=0, velocity=100, pitch=midi.G_3))
			elif elementCount == 3:
				track.append(midi.NoteOnEvent(tick=0, velocity=100, pitch=midi.E_3))
			else:
				track.append(midi.NoteOnEvent(tick=0, velocity=100, pitch=midi.C_3))

		else:
			lineToPrint += '.'

		elementCount += 1

	movedOnYet = False
	elementCount = 0

	for element in elements:
		if element == True:
			if movedOnYet == True:
				ticks = 0
			else:
				ticks = noteLength

			if elementCount == 0:
				track.append(midi.NoteOffEvent(tick=ticks, pitch=midi.E_4))
			elif elementCount == 1:
				track.append(midi.NoteOffEvent(tick=ticks, pitch=midi.C_4))
			elif elementCount == 2:
				track.append(midi.NoteOffEvent(tick=ticks, pitch=midi.G_3))
			elif elementCount == 3:
				track.append(midi.NoteOffEvent(tick=ticks, pitch=midi.E_3))
			else:
				track.append(midi.NoteOffEvent(tick=ticks, pitch=midi.C_3))

			movedOnYet = True

		elementCount += 1

	print lineToPrint

track.append(midi.EndOfTrackEvent(tick=1))
midi.write_midifile('baudot.mid', pattern)
print 'Exported baudot.mid'
