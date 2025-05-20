#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qse_experiments_10000.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QSE na instanci velikosti 
# 10000.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qse"
FILE_PATH="datasets/1000.txt"
POP_SIZES=(5)
VELOCITIES=(1)
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for VELOCITY in "${VELOCITIES[@]}"; do
        echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE a počáteční rychlost: $VELOCITY."
        $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --velocity $VELOCITY --evaluations $EVAL_LIMIT --experiments $EXPERIMENTS --output $OUTPUT
    done
done

