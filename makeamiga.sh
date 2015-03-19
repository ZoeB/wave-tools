#!/bin/sh

for file in *.wav
do
	sox --norm "${file}" -b 8 --rate 8363 "${file%.wav}-amiga.wav"
	rm "${file}"
	mv "${file%.wav}-amiga.wav" "${file}"
done
