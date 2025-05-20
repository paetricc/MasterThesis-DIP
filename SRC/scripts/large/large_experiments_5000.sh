#!/bin/bash

######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: large_experiments_5000.sh
# Popis:
# Skript spouštějící experimenty pro
# všechny algoritmy na instanci 5000. 
# Každý běh je spuštěn na pozadí
# s nižší prioritou a výstup je uložen 
# do složky "logs".
######################################

SCRIPT="python3 src/qiea.py"
OUTPUT="outputs"
FILE_PATH="datasets/5000.txt"
INSTANCE=5000
EVAL_LIMIT=10000
EXPERIMENTS=30
LOG_DIR="logs"

for ((i=1; i<=EXPERIMENTS; i++)); do
    echo "Spouštění QIGA experimentu  číslo: $i"
    nohup nice $SCRIPT "qiga" $FILE_PATH --evaluations $EVAL_LIMIT --experiments 1 --population 1 --magnitude 0.002 --output $OUTPUT --append_results > "$LOG_DIR/qiga_${INSTANCE}_run${i}.log" 2>&1 &

    echo "Spouštění QISA experimentu  číslo: $i"
    nohup nice $SCRIPT "qisa" $FILE_PATH --evaluations $EVAL_LIMIT --experiments 1 --population 1 --cooling "rec-logarithmic" --observation "sigmoid" --output $OUTPUT --append_results > "$LOG_DIR/qisa_${INSTANCE}_run${i}.log" 2>&1 &

    echo "Spouštění QSE experimentu  číslo: $i"
    nohup nice $SCRIPT "qse" $FILE_PATH --evaluations $EVAL_LIMIT --experiments 1 --population 5 --velocity 1 --output $OUTPUT --append_results > "$LOG_DIR/qse_${INSTANCE}_run${i}.log" 2>&1 &
    
    echo "Spouštění QIPSO experimentu  číslo: $i"
    nohup nice $SCRIPT "qipso" $FILE_PATH --evaluations $EVAL_LIMIT --experiments 1 --population 5 --friction 0.01 --c1 0.5 --c2 0.25 --velocity 100 --output $OUTPUT --append_results > "$LOG_DIR/qipso_${INSTANCE}_run${i}.log" 2>&1 &
done