#!/bin/sh
sox $1 ${1%.wav}-.wav silence 1 0.125 1% 1 0.125 1% : newfile : restart
