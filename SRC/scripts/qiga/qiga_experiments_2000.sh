#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qiga_experiments_2000.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QIGA na instanci velikosti 
# 2000.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qiga"
FILE_PATH="datasets/2000.txt"
POP_SIZES=(1)
MAGNITUDES=(0.002)
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for THETA in "${THETAS[@]}"; do
        echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE a parametr theta: $THETA."
        $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --evaluations $EVAL_LIMIT \
            --experiments $EXPERIMENTS  --magnitude $THETA --output $OUTPUT
    done
done
