#!/bin/sh

for file in *.wav
do
	sox $file -b 8 --rate 8363 ${file%.wav}-8363hz.wav
	rm $file
	mv ${file%.wav}-8363hz.wav $file
done

