#!/bin/sh

. ../ylimits
XLIM="-l xy -x 650,350000 -X 1000,10000,100000"
FILES="-f out/4.out -f out/4_unopt.out -f out/4_bccgp.out -f out/4_bullet.out -Z -m 11"

../plot.py ${FILES} $YLIM1 $XLIM -o ../lanczos2_size.pdf

../plot.py ${FILES} $YLIM2 $XLIM -o ../lanczos2_ptime.pdf

../plot.py ${FILES} $YLIM3 $XLIM -o ../lanczos2_vtime.pdf

for i in size ptime vtime; do
    pdfcrop ../lanczos2_${i}.pdf ../lanczos2_${i}.pdf
done
