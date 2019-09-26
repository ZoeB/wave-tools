#!/bin/sh

for file in *.wav
do
	sox $file --norm -b 16 ${file%.wav}-16bit.wav
	rm $file
	mv ${file%.wav}-16bit.wav $file
done
