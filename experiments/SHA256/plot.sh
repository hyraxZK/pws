#!/bin/bash

set -u
set -e

. ../ylimits
XLIM="-l Xy -x 0.5,8.5"
FILES="-f out/merkle.out -f out/merkle_unopt.out -f out/merkle_bccgp.out -f out/merkle_bullet.out -Z -m 11 -G"

../plot.py ${FILES} $YLIM1 $XLIM -o ../sha256_size.pdf

../plot.py ${FILES} $YLIM2 $XLIM -o ../sha256_ptime.pdf

../plot.py ${FILES} $YLIM3 $XLIM -o ../sha256_vtime.pdf

ALLFILES=$(for i in 3 2 0; do echo -f out/merkle_w${i}.out; done | xargs)
LEGEND="-g 2 -L Hyrax-$\nicefrac{1}{3}$ -L Hyrax-$\nicefrac{1}{2}$ -L Hyrax-log"
../plot.py ${ALLFILES} $YLIM4 $XLIM -M ${LEGEND} -o ../merkle_w_size.pdf
../plot.py ${ALLFILES} $YLIM5 $XLIM -M ${LEGEND} -o ../merkle_w_ptime.pdf
../plot.py ${ALLFILES} $YLIM6 $XLIM -M ${LEGEND} -o ../merkle_w_vtime.pdf

for i in size ptime vtime; do
    pdfcrop ../sha256_${i}.pdf ../sha256_${i}.pdf
    pdfcrop ../merkle_w_${i}.pdf ../merkle_w_${i}.pdf
done
