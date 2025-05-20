#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qipso_experiments_5000.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QIPSO na instanci velikosti 
# 5000.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qipso"
FILE_PATH="datasets/5000.txt"
POP_SIZES=(5)
FRICTIONS=(0.01)
COGNITIVE_COEFFICIENTS=(0.5)
SOCIAL_COEFFICIENTS=(0.25)
VELOCITIES=(100)
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for FRICTION in "${FRICTIONS[@]}"; do
        for COGNITIVE in "${COGNITIVE_COEFFICIENTS[@]}"; do
            for SOCIAL in "${SOCIAL_COEFFICIENTS[@]}"; do
                for VELOCITY in "${VELOCITIES[@]}"; do
                    echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE, parametr omega: $FRICTION, kognitivní koeficient: $COGNITIVE, sociální koeficient: $SOCIAL a počáteční rychlost: $VELOCITY."
                    $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --evaluations $EVAL_LIMIT \
                        --experiments $EXPERIMENTS --omega $FRICTION --c1 $COGNITIVE --c2 $SOCIAL --velocity $VELOCITY --output $OUTPUT
                done
            done
        done
    done
done