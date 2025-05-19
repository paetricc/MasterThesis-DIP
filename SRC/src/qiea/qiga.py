######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qiga.py             
# Popis:
# Soubor implementující kvantově 
# inspirovaný evoluční algoritmus
######################################

import numpy as np
from typing import List, Tuple

from qiea.operations import observe, repair, fitness


def qiga(
        item_values: List[int], 
        item_weights: List[int], 
        knapsack_capacity: int, 
        population_size: int, 
        num_generations: int,
        theta: float = 0.01
    ) -> Tuple[float, List[int], List[int], List[float]] :
    """
    Implementace kvantově inspirovaného evolučního algoritmu

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
        theta (float): 
            Parametr theta (výchozí: 0,01)

    Returns:
        Tuple[float, List[int], List[float]]:
            - Nejlepší fitness hodnota dosažená algoritmem.
            - Binární řešení problému reprezentující nejlepší nalezené řešení.
            - Fitness historie nejlepšího nalezeného řešení.
    """
    num_items: int           = np.size(item_values)
    item_values: np.ndarray  = np.array(item_values)
    item_weights: np.ndarray = np.array(item_weights)
    # Inicializace populací
    quantum_population: np.ndarray       = np.full((population_size, num_items, 2), 1/(2**0.5))
    observed_population: np.ndarray      = np.zeros((population_size, num_items), dtype=int)
    personal_best_population: np.ndarray = np.zeros((population_size, num_items), dtype=int)
    # Inicializace fitness
    best_population_fitness: np.ndarray  = np.zeros(population_size)
    current_fitness: np.ndarray          = np.zeros(population_size)
    fitness_histories: np.ndarray = np.zeros((population_size, num_generations), dtype=float)
    # Přepočítání konstant
    positive_theta: float =  theta * np.pi
    negative_theta: float = -theta * np.pi
    cos_positive_theta: float = np.cos(positive_theta) 
    sin_positive_theta: float = np.sin(positive_theta)
    cos_negative_theta: float = np.cos(negative_theta) 
    sin_negative_theta: float = np.sin(negative_theta)

    for generation in range(num_generations):
        # Pozorování kvantové populace
        observed_population: np.ndarray = np.array([observe(individual) for individual in quantum_population])
        # Oprava pozorované kvantové populace
        observed_population: np.ndarray = np.array([repair(individual, item_values, item_weights, knapsack_capacity) for individual in observed_population])
        # Ohodnocení pozorované populace
        current_fitness: np.ndarray = np.array([fitness(individual, item_values) for individual in observed_population])
        # Aktualizace fitness historie každého jedince
        fitness_histories[:, generation] = current_fitness
        # Aktualizace kvantových stavů
        better_fitness_mask: np.ndarray = current_fitness < best_population_fitness
        difference_mask: np.ndarray     = observed_population ^ personal_best_population
        update_state_mask: np.ndarray   = better_fitness_mask[:, None] & difference_mask
        # Initialize theta
        theta_mask: np.ndarray = np.zeros((population_size, num_items), dtype=float)
        # Určení směru rotace o úhel theta
        theta_mask[np.where(update_state_mask & (observed_population == 0))] = positive_theta
        theta_mask[np.where(update_state_mask & (observed_population == 1))] = negative_theta
        # Aplikace kvantového rotačního hradla
        alpha: np.ndarray = quantum_population[:, :, 0] 
        beta: np.ndarray  = quantum_population[:, :, 1]
        pos_mask: np.ndarray = theta_mask == positive_theta
        neg_mask: np.ndarray = theta_mask == negative_theta
        # Aktualizace vybraných koeficientů o +theta
        alpha[pos_mask], beta[pos_mask] = (
            alpha[pos_mask] * cos_positive_theta - beta[pos_mask] * sin_positive_theta,
            alpha[pos_mask] * sin_positive_theta + beta[pos_mask] * cos_positive_theta
        )
        # Aktualizace vybraných koeficientů o -theta
        alpha[neg_mask], beta[neg_mask] = (
            alpha[neg_mask] * cos_negative_theta - beta[neg_mask] * sin_negative_theta,
            alpha[neg_mask] * sin_negative_theta + beta[neg_mask] * cos_negative_theta
        )
        # Uložení nových pravděpodobnostních koeficientů
        quantum_population[:, :, 0], quantum_population[:, :, 1] = alpha, beta
        # Získání nových nejlepších řešení
        better_fitness_indices: np.ndarray = current_fitness > best_population_fitness
        personal_best_population[better_fitness_indices] = observed_population[better_fitness_indices]
        best_population_fitness[better_fitness_indices] = current_fitness[better_fitness_indices]
    # Nalezení nejlepšího řešení a jeho fitness
    best_fitness: float = np.max(best_population_fitness)
    best_index: int = np.argmax(best_population_fitness)
    best_chromosome: np.ndarray = personal_best_population[best_index].tolist()
    best_fitness_history: np.ndarray = fitness_histories[best_index, :].tolist()

    return best_fitness, best_chromosome, best_fitness_history
