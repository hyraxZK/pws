#!/bin/bash

mkdir -p out
XLABEL="high-resolution image size, pixels"

process_file () {
    echo ${XLABEL} > out/${oname}.out
    for NPIXELS in "${psizes[@]}"; do
        LOGFILE=(${logdir}/lanczos2_${dres}_${NPIXELS}_*.log)
        readarray -t -n 4 RESULTS < <(egrep '^Proof size|^Prover runtime|^Verifier runtime|^Max memory' ${LOGFILE[0]})
        NCOPIES=${LOGFILE[0]##*_N=}
        NCOPIES=${NCOPIES%.log}
        PROOFSIZE=${RESULTS[0]##* size: }
        PROOFSIZE=${PROOFSIZE%% *}
        PTIME=${RESULTS[1]##* }
        VTIME=${RESULTS[2]##* }
        MAXMEM=${RESULTS[3]##*usage: }
        MAXMEM=${MAXMEM%% *}
        # don't echo $NCOPIES, not important
        echo $(($NPIXELS**2)) $PROOFSIZE $PTIME $VTIME $MAXMEM
    done >> out/${oname}.out
}


dres=4
logdir=log
oname=4
psizes=(28 44 76 140 268 524)
process_file

for w in bccgp bullet unopt; do
    oname=4_${w}
    logdir=log_${w}
    process_file
done
