#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qisa_experiments_2000.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QISA na instanci velikosti 
# 2000.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qisa"
FILE_PATH="datasets/2000.txt"
POP_SIZES=(1)
COOLING_METHODS=("rec-logarithmic")
OBSERVATION_METHODS=("sigmoid")
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for COOLING in "${COOLING_METHODS[@]}"; do
        for OBSERVATION in "${OBSERVATION_METHODS[@]}"; do
            echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE, chladicí schéma: $COOLING a pozorovací metodu: $OBSERVATION."
            $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --evaluations $EVAL_LIMIT \
                --experiments $EXPERIMENTS --cooling $COOLING --observation $OBSERVATION \
                --output $OUTPUT
        done
    done
done