######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qisa.py             
# Popis:
# Soubor implementující kvantově 
# inspirované simulované žíhání
######################################

import numpy as np
from typing import List, Tuple

from qiea.operations import heated_observe, repair, fitness, initial_temperature, update_temperature


def qisa(
        item_values: List[int], 
        item_weights: List[int], 
        knapsack_capacity: int, 
        population_size: int, 
        num_generations: int, 
        cooling_rate: float = 0.98,
        observation: str = "sigmoid",
        cooling: str = "rec-logarithmic"
    ) -> Tuple[float, List[int], List[float]]:
    """
    Implementace kvantově inspirovaného simulovaného žíhání

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
        cooling_rate (float): 
            Míra ochlazování (výchozí 0,98)
        observation_method (str): 
            Výběr pozorovací metody ("sigmoid" nebo "constant") (výchozí: sigmoid)
        cooling (str): 
            Výběr chladicího plánu ("exponential", "linear","logarithmic" nebo "rec-logarithmic") (výchozí: rec-logarithmic)

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
    quantum_population: np.ndarray = np.full((population_size, num_items, 2), 1 / np.sqrt(2))
    observed_population: np.ndarray = np.zeros((population_size, num_items), dtype=int)
    personal_best_population: np.ndarray = np.zeros((population_size, num_items), dtype=int)
    # Inicializace fitness
    best_population_fitness: np.ndarray  = np.zeros(population_size, dtype=float)
    current_fitness: np.ndarray          = np.zeros(population_size, dtype=float)
    fitness_histories: np.ndarray        = np.zeros((population_size, num_generations), dtype=float)
    # Inicializace teplot
    initial_temp = int(initial_temperature(item_values, item_weights, knapsack_capacity))
    temperature = initial_temp
    # Pozorování kvantové populace
    observed_population = heated_observe(quantum_population, temperature, observation, w=9/num_items, w1=50, w2=0.2, w3=9/num_items, w4=9/num_items, T0=initial_temp)
    # Oprava pozorované kvantové populace
    observed_population: np.ndarray = np.array([repair(individual, item_values, item_weights, knapsack_capacity) for individual in observed_population])
    # Ohodnocení pozorované populace
    previous_fitness: np.ndarray = np.array([fitness(individual, item_values) for individual in observed_population])

    for generation in range(num_generations):
        # Pozorování kvantové populace
        observed_population = heated_observe(quantum_population, temperature, observation, w=9/num_items, w1=50, w2=0.2, w3=9/num_items, w4=9/num_items, T0=initial_temp)
        # Oprava pozorované kvantové populace
        observed_population: np.ndarray = np.array([repair(individual, item_values, item_weights, knapsack_capacity) for individual in observed_population])
        # Ohodnocení pozorované populace
        current_fitness: np.ndarray = np.array([fitness(individual, item_values) for individual in observed_population])
        # Apply quantum update if fitness improves
        improvement_mask = current_fitness >= previous_fitness
        quantum_population[improvement_mask, :, 0] = 1 - observed_population[improvement_mask]
        quantum_population[improvement_mask, :, 1] = observed_population[improvement_mask]
        # Aktualizace přecházející fitness (energie) pro řešení, která se zlepšují
        previous_fitness[improvement_mask] = current_fitness[improvement_mask]
        # Výpočet faktoru 'b'
        non_improvement_mask = ~improvement_mask
        b = np.exp((current_fitness[non_improvement_mask] - previous_fitness[non_improvement_mask]) / max(temperature, 1))
        # Výpočet úhlu rotace
        delta_theta = b[:, np.newaxis] * ((np.pi / 2) * observed_population[non_improvement_mask] - np.arctan2(quantum_population[non_improvement_mask, :, 1], quantum_population[non_improvement_mask, :, 0]))
        cos_theta, sin_theta = np.cos(delta_theta), np.sin(delta_theta)
        # Aplikace kvantového rotačního hradla
        alpha, beta = quantum_population[non_improvement_mask, :, 0], quantum_population[non_improvement_mask, :, 1]
        quantum_population[non_improvement_mask, :, 0] = alpha * cos_theta - beta * sin_theta
        quantum_population[non_improvement_mask, :, 1] = alpha * sin_theta + beta * cos_theta
        # Aktualizace přecházející fitness (energie) pro řešení, která se nezlepšují
        previous_fitness[non_improvement_mask] = np.cos(b * np.pi / 2) ** 2 * previous_fitness[non_improvement_mask] + np.sin(b * np.pi / 2) ** 2 * current_fitness[non_improvement_mask]
        # Aplikace chlazení
        temperature = update_temperature(temperature, initial_temp, generation, cooling, cooling_rate)
        # Aktualizace fitness historie každého jedince
        fitness_histories[:, generation] = previous_fitness
        # Získání nových nejlepších řešení
        better_mask: np.ndarray = current_fitness > best_population_fitness
        personal_best_population[better_mask] = observed_population[better_mask]
        best_population_fitness[better_mask] = current_fitness[better_mask]
    # Nalezení nejlepšího řešení a jeho fitness
    best_fitness: float = np.max(best_population_fitness)
    best_index: int = np.argmax(best_population_fitness)
    best_chromosome: np.ndarray = personal_best_population[best_index].tolist()
    best_fitness_history: np.ndarray = fitness_histories[best_index, :].tolist()

    return best_fitness, best_chromosome, best_fitness_history
