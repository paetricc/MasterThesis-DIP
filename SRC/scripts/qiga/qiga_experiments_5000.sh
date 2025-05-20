#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qiga_experiments_5000.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QIGA na instanci velikosti 
# 5000.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qiga"
FILE_PATH="datasets/5000.txt"
POP_SIZES=(1)
THETAS=(0.002)
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for THETA in "${THETAS[@]}"; do
        echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE a parametr theta: $THETA."
        $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --evaluations $EVAL_LIMIT \
            --experiments $EXPERIMENTS  --theta $THETA --output $OUTPUT
    done
done
