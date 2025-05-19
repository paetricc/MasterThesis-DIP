######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qse.py             
# Popis:
# Soubor implementující kvantovou
# evoluci roje
######################################

import numpy as np
from typing import List, Tuple

from qiea.operations import repair, fitness, angle_observe


def qse(
        item_values: List[int], 
        item_weights: List[int], 
        knapsack_capacity: int, 
        population_size: int, 
        num_generations: int,
        velocity: float = 1.0
    ) -> Tuple[float, List[int], List[float]]:
    """
    Implementace kvantové evoluce roje

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
    quantum_angles: np.ndarray           = np.full((population_size, num_items), np.pi / 4)
    observed_population: np.ndarray      = np.zeros((population_size, num_items), dtype=int)
    # Inicializace osobních nejlepších řešení
    personal_best_population: np.ndarray = np.zeros((population_size, num_items), dtype=int)
    personal_best_angles: np.ndarray     = quantum_angles.copy()
    # Inicializace rychlosti
    velocities: np.ndarray               = np.full((population_size, num_items), fill_value=velocity, dtype=float)
    # Inicializace fitness
    best_population_fitness: np.ndarray  = np.zeros(population_size, dtype=float)
    fitness_histories: np.ndarray        = np.zeros((population_size, num_generations), dtype=float)
    # Inicializace globálního nejlepšího řešení
    global_best_fitness: float           = -np.inf
    global_best_angles: np.ndarray       = np.zeros(num_items, dtype=float)
    # Předpočítání konstant
    max_velocity: float                  = np.pi / 2
    # Parametry dané algoritmem
    chi: float   = 0.99
    omega: float = 0.7298
    C1: float    = 1.42
    C2: float    = 1.57

    for generation in range(num_generations):
        # Pozorování kvantové populace
        observed_population = np.array([angle_observe(ind) for ind in quantum_angles])
        # Oprava pozorované kvantové populace
        observed_population = np.array([repair(ind, item_values, item_weights, knapsack_capacity) for ind in observed_population])
        # Ohodnocení pozorované populace
        current_fitness = np.array([fitness(ind, item_values) for ind in observed_population])
        # Aktualizace fitness historie každého jedince
        fitness_histories[:, generation] = current_fitness
        # Aktualizace nejlepších osobních řešení
        better_mask: np.ndarray = current_fitness > best_population_fitness
        personal_best_population[better_mask] = observed_population[better_mask]
        personal_best_angles[better_mask] = quantum_angles[better_mask]
        best_population_fitness[better_mask] = current_fitness[better_mask]
        # Aktualizace globálního nejlepšího řešení
        max_idx = np.argmax(best_population_fitness)
        if best_population_fitness[max_idx] > global_best_fitness:
            global_best_fitness = best_population_fitness[max_idx]
            global_best_angles = personal_best_angles[max_idx]
        # Aktualizace rychlostí
        r1 = np.random.uniform(0, 1, (population_size, num_items))
        r2 = np.random.uniform(0, 1, (population_size, num_items))
        velocities = chi * (
            omega * velocities +
            C1 * r1 * (personal_best_angles - quantum_angles) +
            C2 * r2 * (global_best_angles - quantum_angles)
        )
        # Omezení maximální rychlosti
        velocities = np.clip(velocities, -max_velocity, max_velocity)
        # Aktualizace kvantových úhlů
        quantum_angles = quantum_angles + velocities
    # Nalezení nejlepšího řešení a jeho fitness
    best_fitness = np.max(best_population_fitness)
    best_index = np.argmax(best_population_fitness)
    best_chromosome = personal_best_population[best_index].tolist()
    best_fitness_history = fitness_histories[best_index, :].tolist()

    return best_fitness, best_chromosome, best_fitness_history
