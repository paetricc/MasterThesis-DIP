#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qisa_experiments_100.sh           
# Popis:
# Skript spouštějící experimenty 
# algoritmu QISA na instanci velikosti 
# 100.
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
ALGORITHM="qisa"
FILE_PATH="datasets/100.txt"
POP_SIZES=(1 5 10 20 30 40 50 100)
COOLING_METHODS=("exponential" "linear" "logarithmic" "rec-logarithmic")
COOLING_RATES=(0.90 0.95 0.98 0.99)
OBSERVATION_METHODS=("constant" "sigmoid")
EVAL_LIMIT=10000
EXPERIMENTS=30

for POP_SIZE in "${POP_SIZES[@]}"; do
    for COOLING in "${COOLING_METHODS[@]}"; do
        for RATE in "${COOLING_RATES[@]}"; do
            for OBSERVATION in "${OBSERVATION_METHODS[@]}"; do
                echo "Spouštění experimentů pro populaci velikosti: $POP_SIZE, chladicí schéma: $COOLING, míru ochlazování: $RATE, a pozorovací metodu: $OBSERVATION."
                $SCRIPT $ALGORITHM $FILE_PATH --population $POP_SIZE --evaluations $EVAL_LIMIT \
                    --experiments $EXPERIMENTS --cooling $COOLING --cooling_rate $RATE --observation $OBSERVATION \
                    --output $OUTPUT
            done
        done
    done
done