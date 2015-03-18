#!/bin/sh

for file in *.wav
do
	sox --norm $file -b 16 --rate 44100 ${file%.wav}-cd.wav
	rm $file
	mv ${file%.wav}-cd.wav $file
done
