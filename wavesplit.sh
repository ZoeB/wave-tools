#!/bin/sh

sox $1  ${1%.*}-.${1##*.} silence 1 0.125 1% 1 0.125 0.25% : newfile : restart
