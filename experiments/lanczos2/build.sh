#!/bin/sh

( for i in 14 22 38 70 134 262 518 1030; do ../../lanczos2.py 2 $i; done ) &

( for i in 28 44 76 140 268 524 1036; do ../../lanczos2.py 4 $i; done ) &

( for i in 56 88 152 280 536 1048; do ../../lanczos2.py 8 $i; done ) &

for i in 112 176 304 560 1072; do ../../lanczos2.py 16 $i; done
