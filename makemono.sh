#!/bin/sh

for file in *.wav
do
	sox "$file" -c 1 "${file%.wav}-mono.wav" remix 1
	rm "$file"
	mv "${file%.wav}-mono.wav" "$file"
done
