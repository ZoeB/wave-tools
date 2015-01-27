#!/bin/sh

for file in *.WAV
do
	mv $file ${file%.WAV}.wav
done
