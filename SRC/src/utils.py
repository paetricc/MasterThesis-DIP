######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: utils.py             
# Popis:
# Pomocné funkce pro práci se soubory
# spolu s výpočtem počtu generací 
# algoritmu
######################################

import numpy as np
import os

from typing import List


def load_knapsack_data(file_path):
    """
    Funkce pro načtení datové sady.

    Soubor by měl mít následující formát:
    - První řádek obsahuje kapacitu batohu a název datové sady
    - Každý další řádek obsahuje hodnotu a váhu jednoho předmětu.

    Parameters:
        file_path (str): 
            Cesta k souboru s daty

    Returns:
        tuple(np.ndarray, np.ndarray, int, str):
            - Hodnoty položek
            - Váhy položek
            - Kapacita batohu
            - Název datové sady
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    first_line = lines[0].strip().split()
    capacity = int(first_line[0])
    dataset = first_line[1]

    data = np.loadtxt(lines[1:], dtype=int, delimiter=" ")
    profits = data[:, 0]
    weights = data[:, 1]

    return profits, weights, capacity, dataset


def save_results(algorithm: str, dataset_name: str, results: List[float], output_dir: str, append: bool, **params):
    """
    Funkce pro uložení výsledků do .CSV souboru

    Parameters:
        algorithm (str): 
            Název použitého algoritmu
        dataset_name (str): 
            Název datové sady
        results (List[float]): 
            Seznam výsledků, kde:
            - 'fitness' (float): Nejlepší dosažená fitness
            - 'chromosome' (List[int]): Binární reprezentace nejlepšího řešení
            - 'fitness_history' (List[float]): Historie fitness nejlepšího řešení
        output_dir (str): 
            Cesta k výstupní složce
        append (bool): 
            Rozhodnutí zde se připojí výsledky na konec existujícího souboru
        **params: 
            Dodatečné parametry algoritmu, které budou použity v názvu souboru
    """
    os.makedirs(output_dir, exist_ok=True)

    params_str = "_".join(f"{key.replace('_', '')}:{value}" for key, value in params.items() if value is not None)
    output_file = os.path.join(output_dir, f"{algorithm.upper()}_{dataset_name}_{params_str}.csv")

    file_exists = os.path.exists(output_file)
    mode = "a" if append else "w"

    with open(output_file, mode=mode) as file:
        if not file_exists or not append:
            file.write("Experiment,Fitness,Chromosome,FitnessHistory\n")
        
        for idx, result in enumerate(results, start=1):
            chromosome_str = ";".join(map(str, result["chromosome"]))
            fitness_history_str = ";".join(map(str, result["fitness_history"]))
            file.write(f"{idx},{result['fitness']},{chromosome_str},{fitness_history_str}\n")

    print(f"Výsledky byly uloženy do: {output_file}")


def calculate_iterations(eval_limit, population_size, elite_count=0):
    """
    Funkce pro výpočet počtu iterací (generací) evolučního algoritmu.

    Parameters:
        eval_limit (int): 
            Maximální počet vyhodnocení fitness funkce
        population_size (int): 
            Počet jedinců v populaci.
        elite_count (int): 
            Počet elitních jedinců (výchozí: 0)

    Returns:
        int: maximální počet iterací
    """
    return (eval_limit - elite_count) // population_size
