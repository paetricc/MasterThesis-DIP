#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qiga_experiments_100.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QIGA na instanci velikosti 
# 100.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qiga"
FILE_PATH="datasets/100.txt"
POP_SIZES=(1 5 10 20 30 40 50 100)
THETAS=(0.002 0.01 0.05 0.1 0.2 0.5 1 2)
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for THETA in "${THETAS[@]}"; do
        echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE a parametr theta: $THETA."
        $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --evaluations $EVAL_LIMIT \
            --experiments $EXPERIMENTS  --magnitude $THETA --output $OUTPUT
    done
done
