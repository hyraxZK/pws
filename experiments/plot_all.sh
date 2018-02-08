#!/bin/bash

exec 3< <( cd lanczos2 ; ./process.sh ; ./plot.sh )
exec 4< <( cd matmult ; ./process.sh ; ./plot.sh )
exec 5< <( cd SHA256 ; ./process.sh ; ./plot.sh )

LEGEND="-L Hyrax-$\nicefrac{1}{2}$ -L Hyrax-$\nicefrac{1}{3}$ -L Hyrax-naive -L BCCGP-sqrt -L Bulletproofs -L ZKB++ -L Ligero"
FILES="-f SHA256/out/merkle.out -f SHA256/out/merkle.out $(for i in unopt bccgp bullet zkbpp ligero; do echo "-f SHA256/out/merkle_${i}.out" ; done | xargs)"
./plot.py ${LEGEND} ${FILES} -H -o legend.pdf
pdfcrop --bbox "60 896 1410 955" legend.pdf legend.pdf
pdfcrop legend.pdf legend.pdf

# wait for the subshells to finish
cat <&3
cat <&4
cat <&5
