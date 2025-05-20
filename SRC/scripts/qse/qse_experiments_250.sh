#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qse_experiments_250.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QSE na instanci velikosti 
# 250.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qse"
FILE_PATH="datasets/250.txt"
POP_SIZES=(1 5 10 20 30 40 50 100)
VELOCITIES=(0 1 2 5 10 25 50 100)
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for VELOCITY in "${VELOCITIES[@]}"; do
        echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE a počáteční rychlost: $VELOCITY."
        $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --velocity $VELOCITY --evaluations $EVAL_LIMIT --experiments $EXPERIMENTS --output $OUTPUT
    done
done

