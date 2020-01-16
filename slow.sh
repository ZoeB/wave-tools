#!/bin/sh

# Slow down a recording to 3/4 speed
# 45 RPM to 33.(3) RPM is 0.74 speed
# Five semitones lower is 0.75 speed

for file in *.flac
do
	sox "$file" "${file%.wav}-slow.wav" speed 0.75
	rm "$file"
	mv "${file%.wav}-slow.wav" "$file"
done
