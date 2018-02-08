#!/bin/bash

RUN="pypy -OO ../../../fennel/run_fennel.py -z 3 -C m191 -n 0"
mkdir -p log

# # run tests for 2x downscaling
# echo "running 2x downscaling tests"
# for i in $(seq 4 2 18); do
# 	RDLFILE=lanczos2_2_*$((2**${i}))_rdl.pws
# 	LOGFILE=$(basename ${RDLFILE} _rdl.pws).log
# 	echo "** "${RDLFILE}
# 	${RUN} -p lanczos2_2.pws -r ${RDLFILE} -c ${i} -L log/${LOGFILE}
# done

# run tests for 4x downscaling
echo "running 4x downscaling tests"
for i in $(seq 4 2 14); do
	RDLFILE=lanczos2_4_*$((2**${i}))_rdl.pws
	LOGFILE=$(basename ${RDLFILE} _rdl.pws).log
	echo "** "${RDLFILE}
	${RUN} -p lanczos2_4.pws -r ${RDLFILE} -c ${i} -L log/${LOGFILE}
done

# # run tests for 8x downscaling
# echo "running 8x downscaling tests"
# for i in $(seq 4 2 14); do
# 	RDLFILE=lanczos2_8_*$((2**${i}))_rdl.pws
# 	LOGFILE=$(basename ${RDLFILE} _rdl.pws).log
# 	echo "** "${RDLFILE}
# 	${RUN} -p lanczos2_8.pws -r ${RDLFILE} -c ${i} -L log/${LOGFILE}
# done
# 
# 
# # run tests for 16x downscaling
# echo "running 16x downscaling tests"
# for i in $(seq 4 2 12); do
# 	RDLFILE=lanczos2_16_*$((2**${i}))_rdl.pws
# 	LOGFILE=$(basename ${RDLFILE} _rdl.pws).log
# 	echo "** "${RDLFILE}
# 	${RUN} -p lanczos2_16.pws -r ${RDLFILE} -c ${i} -L log/${LOGFILE}
# done
