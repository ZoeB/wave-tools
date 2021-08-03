#!/bin/sh

for file in *.wav
do
	sox --norm "${file}" -b 24 --rate 48000 "${file%.wav}-2448.wav"
	rm "${file}"
	mv "${file%.wav}-2448.wav" "${file}"
done
