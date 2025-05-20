######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: operations.py             
# Popis:
# Soubor implementující různé operace
# nutné pro výpočet kvantově 
# inspirovaných evolučních algoritmů 
# a to:
# * fitness funkce
# * oprava batohu
# * kvantová pozorování
# * výpočet iniciální teploty
# * aktualizace teploty
######################################

import numpy as np


def fitness(chromosome: np.ndarray, item_values: np.ndarray):
    """
    Funkce pro výpočet fitness hodnoty pozorovaného chromozomu.

    Parameters:
        chromosome (np.ndarray):
            Pozorovaný kvantový chromozom
        item_values:
            Pole hodnot jednotlivých položek

    Returns:
        float: Fitness hodnota
    """
    return np.dot(chromosome, item_values)


def repair(chromosome: np.ndarray, item_values: np.ndarray, item_weights: np.ndarray, knapsack_capacity: int):
    """
    Oprava binárního chromozomu hladovou metodou

    Parameters:
        chromosome (np.ndarray): 
            Pozorovaný kvantový chromozom
        item_values (np.ndarray): 
            Pole hodnot jednotlivých položek.
        item_weights (np.ndarray): 
            Pole vah jednotlivých položek.
        knapsack_capacity (int): 
            Kapacita batohu
    
    Returns:
        np.ndarray: Opravený chromozom
    """
    while np.dot(item_weights, chromosome) > knapsack_capacity:
        temp = np.multiply(item_weights / item_values, chromosome)
        chromosome[np.argmax(temp)] = 0
    
    while np.dot(item_weights, chromosome) <= knapsack_capacity:
        temp = np.multiply(item_weights / item_values, 1 - chromosome)
        chromosome[np.argmax(temp)] = 1
    
    chromosome[np.argmax(temp)] = 0
    return chromosome


def observe(chromosome: np.ndarray):
    """
    Funkce, jež generuje řešení pomocí pozorování kvantového chromozomu

    Parameters:
        chromosome (np.ndarray): 
            Kvantový chromozom, jenž má být pozorován

    Returns:
        np.ndarray: Pozorovaný kvantový chromozom
    """
    return np.random.rand(len(chromosome)) < np.square(np.array(chromosome)[:, 1])


def heated_observe(quantum_population: np.ndarray, temperature: float, method: str = "constant", w: float = 0.03, w1: float = 10.0, w2: float = 0.5, w3: float = 0.5, w4: float = 0.0, T0: float = 1.0) -> np.ndarray:
    """
    Funkce pro tepelně-řízené pozorování v algoritmu QISA.

    Parameters:
        quantum_population (np.ndarray): 
            Pole kvantových chromozomů
        temperature (float):
            Aktuální teplota
        method (str):
            Pozorovací metoda
        w, w1, w2, w3, w4 (float):
            Konstanty řídící pozorování
        T0 (float):
            Počáteční teplota

    Returns:
        np.ndarray: Pozorovaná řešení.
    """
    if method == "constant":
        h_T = w
    elif method == "sigmoid":
        h_T = (w3 / (1 + np.exp(-w1 * (temperature / T0 - w2)))) + w4
    else:
        raise ValueError("Invalid heating method. Choose 'constant' or 'sigmoid'.")
    
    alpha = quantum_population[:, :, 0] ** 2 + (0.5 - quantum_population[:, :, 0] ** 2) * h_T
    beta = quantum_population[:, :, 1] ** 2 + (0.5 - quantum_population[:, :, 1] ** 2) * h_T
    
    return (np.random.rand(*alpha.shape) < beta).astype(int)


def angle_observe(phi: np.ndarray):
    """
    Funkce pro pozorování kvantového stavu v algoritmu QSE.

    Parameters:
        phi (np.ndarray): 
            Pole kvantových úhlů

    Returns:
        np.ndarray: Pozorovaná řešení.
    """
    return np.random.rand(len(phi)) < np.square(np.cos(phi))


def initial_temperature(item_values: np.ndarray, item_weights: np.ndarray, knapsack_capacity: int, num_samples: int = 1000) -> float:
    """
    Funkce pro výpočet počáteční teploty

    Parameters:
        item_values (List[int]): 
            Seznam hodnot položek
        item_weights (List[int]): 
            Seznam váh položek
        knapsack_capacity (int): 
            Kapacita batohu
        num_samples (int):
            Počet vzorků pro vygenerování

    Returns
        float: Počáteční teplotu
    """
    num_items = len(item_values)
    random_solutions = np.random.randint(0, 2, size=(num_samples, num_items))
    repaired_solutions = np.array([repair(sol, item_values, item_weights, knapsack_capacity) for sol in random_solutions])
    fitness_values = np.array([fitness(sol, item_values) for sol in repaired_solutions])
    return np.std(fitness_values)


def update_temperature(T: float, T_0: float, generation: int, method: str = "rec-logarithmic", cooling_rate: float = 0.98) -> float:
    """
    Funkce pro aktualizaci teploty dle zvoleného chladícího plánu.

    Parameters:
        T (float): 
            Aktuální teplota
        T_0 (float):
            Počáteční teplota
        generation (int):
            Aktuální generace
        method (str):
            Chladicí plán
        cooling_rate (float):
            Míra ochlazování

    Returns:
        float: Nová teplota
    """
    if method == "exponential":
        T *= cooling_rate
    elif method == "linear":
        T -= cooling_rate
        T = max(T, 0)
    elif method == "logarithmic":
        T = T_0 / np.log(2 + generation)
    elif method == "rec-logarithmic":
        T = T / np.log(2 + generation)
    else:
        raise ValueError("Chybně zvolený chladící plán. Možnosti: 'exponential', 'linear', 'logarithmic' nebo 'rec-logarithmic'.")
    return T
