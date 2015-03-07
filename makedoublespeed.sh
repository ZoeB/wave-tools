#!/bin/sh

for file in *.aiff
do
	sox $file ${file%.aiff}-fast.aiff speed 2
done
