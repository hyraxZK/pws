#!/bin/sh

for i in 16 32 64 128; do
    echo $i
done | parallel python ../../matmult.py
