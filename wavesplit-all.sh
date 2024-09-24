#!/bin/sh

for file in *.wav
do
	sox $file  ${file%.*}-.${file##*.} silence 1 0.125 1% 1 0.125 0.25% : newfile : restart
	rm $file
done
