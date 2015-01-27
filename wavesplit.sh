#!/bin/sh

for file in *.wav
do
	sox $file -c 1 ${file%.wav}-.wav remix 1
	sox $file ${file%.wav}-.wav silence 1 0.125 1% 1 0.125 1% : newfile : restart
	rm $file ${file%.wav}-.wav # What is this?
done
