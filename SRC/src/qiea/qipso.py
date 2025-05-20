######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qipso.py             
# Popis:
# Soubor implementující kvantově 
# inspirovanou optimalizaci rojem 
# částic
######################################

import numpy as np
from typing import List, Tuple

from qiea.operations import observe, repair, fitness


def qipso(
        item_values: List[int], 
        item_weights: List[int], 
        knapsack_capacity: int, 
        population_size: int, 
        num_generations: int, 
        cognitive: float = 0.05, 
        social: float = 0.15, 
        omega: float = 0.01,
        velocity: float = 0.0
    ) -> Tuple[float, List[int], List[float]]:
    """
    Implementace kvantově inspirované optimalizace rojem částic

    Parameters:
        item_values (List[int]): 
            Seznam hodnot položek
        item_weights (List[int]): 
            Seznam váh položek
        knapsack_capacity (int): 
            Kapacita batohu
        population_size (int): 
            Počet jedinců v populaci
        num_generations (int): 
            Počet generací evolučního procesu
        cognitive (float): 
            Kognitivní koeficient
        social (float): 
            Sociální koeficient
        omega (float): 
            Parametr zúžení
        velocity (float):
            Počáteční rychlost částice

    Returns:
        Tuple[float, List[int], List[float]]:
            - Nejlepší fitness hodnota dosažená algoritmem.
            - Binární řešení problému reprezentující nejlepší nalezené řešení.
            - Fitness historie nejlepšího nalezeného řešení.
    """    
    num_items = len(item_values)
    item_values: np.ndarray  = np.array(item_values)
    item_weights: np.ndarray = np.array(item_weights)
    # Inicializace populací
    quantum_population: np.ndarray       = np.full((population_size, num_items, 2), 1 / np.sqrt(2))
    observed_population: np.ndarray      = np.zeros((population_size, num_items), dtype=int)
    # Inicializace osobních nejlepších řešení
    personal_best_population: np.ndarray = np.zeros((population_size, num_items), dtype=int)
    # Inicializace rychlosti
    velocities: np.ndarray               = np.full((population_size, num_items), fill_value=velocity, dtype=float)
    # Inicializace fitness
    best_population_fitness: np.ndarray  = np.zeros(population_size, dtype=float)
    current_fitness: np.ndarray          = np.zeros(population_size, dtype=float)
    fitness_histories: np.ndarray        = np.zeros((population_size, num_generations), dtype=float)
    # Inicializace globálního nejlepšího řešení
    global_best_fitness: float           = -np.inf
    global_best_population: np.ndarray   = np.zeros(num_items, dtype=int)
    # Předpočítání konstant
    max_velocity: float                   = np.pi * 0.5

    for generation in range(num_generations):
        # Pozorování kvantové populace
        observed_population: np.ndarray = np.array([observe(individual) for individual in quantum_population])
        # Oprava pozorované kvantové populace
        observed_population: np.ndarray = np.array([repair(individual, item_values, item_weights, knapsack_capacity) for individual in observed_population])
        # Ohodnocení pozorované populace
        current_fitness: np.ndarray = np.array([fitness(individual, item_values) for individual in observed_population])
        # Aktualizace fitness historie každého jedince
        fitness_histories[:, generation] = current_fitness
        # Aktualizace nejlepších osobních řešení
        better_mask: np.ndarray = current_fitness > best_population_fitness
        personal_best_population[better_mask] = observed_population[better_mask]
        best_population_fitness[better_mask] = current_fitness[better_mask]
        # Aktualizace globálního nejlepšího řešení
        max_idx: int = np.argmax(best_population_fitness)
        if best_population_fitness[max_idx] > global_best_fitness:
            global_best_fitness = best_population_fitness[max_idx]
            global_best_population = personal_best_population[max_idx]
        # Aktualizace rychlostí
        r1: float = np.random.uniform(0, 1, (population_size, num_items))
        r2: float = np.random.uniform(0, 1, (population_size, num_items))
        velocities = (
            omega * velocities +
            cognitive * r1 * (personal_best_population - observed_population) +
            social * r2 * (global_best_population - observed_population)
        )
        # Omezení maximální rychlosti
        velocities = np.clip(velocities, -max_velocity, max_velocity)
        # Aplikace kvantového rotačního hradla
        alpha = quantum_population[:, :, 0]
        beta  = quantum_population[:, :, 1]
        # Předpočítání hodnot sin a cos pro danou rychlosst
        sin_theta: np.ndarray = np.sin(velocities)
        cos_theta: np.ndarray = np.cos(velocities)
        # Aktualizace pravděpodobnostních koeficientů
        updated_alpha: np.ndarray = alpha * cos_theta - beta * sin_theta
        updated_beta: np.ndarray  = alpha * sin_theta + beta * cos_theta
        # Uložení nových pravděpodobnostních koeficientů
        quantum_population[:, :, 0] = updated_alpha
        quantum_population[:, :, 1] = updated_beta
    # Nalezení nejlepšího řešení a jeho fitness
    best_fitness: float = np.max(best_population_fitness)
    best_index: int = np.argmax(best_population_fitness)
    best_chromosome: np.ndarray = personal_best_population[best_index].tolist()
    best_fitness_history: np.ndarray = fitness_histories[best_index, :].tolist()
    
    return best_fitness, best_chromosome, best_fitness_history
