#!/bin/sh

for file in *.wav
do
	sox --norm $file ${file%.wav}-loud.wav
	rm $file
	mv ${file%.wav}-loud.wav $file
done
