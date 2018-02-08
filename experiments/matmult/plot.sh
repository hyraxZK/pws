#!/bin/sh

. ../ylimits
XLIM="-l Xy -x 0.5,9.5"
FILES="-f out/64.out -f out/64_unopt.out -f out/64_bccgp.out -f out/64_bullet.out -Z -m 11"

../plot.py ${FILES} ${YLIM1} ${XLIM} -o ../mm_size.pdf

../plot.py ${FILES} ${YLIM2} ${XLIM} -o ../mm_ptime.pdf

../plot.py ${FILES} ${YLIM3} ${XLIM} -o ../mm_vtime.pdf

for i in size ptime vtime; do
    pdfcrop ../mm_${i}.pdf ../mm_${i}.pdf
done
