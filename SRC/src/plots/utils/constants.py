######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: constants.py             
# Popis:
# Soubor obsahující různé konstanty
######################################

# Mapování parametrů experimentů na 
# proměnné pro analýzu a vizualizaci.
PARAM_MAP = {
    "population": int,
    "theta": float,
    "evaluations": int,
    "generations": int,
    "c1": ("cognitive", float),
    "c2": ("social", float),
    "omega": float,
    "mutation": float,
    "crossover": float,
    "numelites": ("elites", float),
    "velocity": float,
    "cooling": str,
    "coolingrate": ("cooling_rate", float),
    "observation": str,
}

# Optimální hodnoty fitness pro
# dané instance problému
OPT_FITNESS = {
    100: 3967,
    250: 10424,
    500: 20925,
    1000: 54503,
    2000: 110625,
    5000: 276457,
    10000: 563647
}