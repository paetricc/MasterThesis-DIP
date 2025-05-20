######################################
# Autor: Tomáš Bártů              
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: qiea.py             
# Popis:
# Vstupní bod pro práci s kvantově 
# inspirovanými evolučními algoritmy
######################################

import argparse

from qiea.qiga import qiga
from qiea.qipso import qipso
from qiea.qse import qse
from qiea.qisa import qisa

from utils import calculate_iterations, load_knapsack_data, save_results


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kvantově inspirované evoluční algoritmy pro řešení problému batohu ve variantě 0-1")
    algorithms  = ["qiga", "qisa", "qse", "qipso"]
    cooling     = ["exponential", "linear", "logarithmic", "rec-logarithmic"]
    observation = ["constant", "sigmoid"]

    parser.add_argument("algorithm",      choices=algorithms,        help="Typ algoritmus pro běh (QIGA, QIPSO, QIDE, GA, PSO)")
    parser.add_argument("input",          type=str,                  help="Cesta ke vstupní datové sadě")
    parser.add_argument("--append_results", action="store_true",     help="Rozhodnutí zda se mají výsledky experimentů připojovat k již existujícím")
    parser.add_argument("--output",       type=str,   default=None,  help="Cesta ke složce pro uložení výsledků experimentů")
    parser.add_argument("--experiments",  type=int,   default=30,    help="Počet nezávislých běhů (výchozí: 30)")
    parser.add_argument("--population",   type=int,   default=1,     help="Velikost populace (výchozí: 1)")
    parser.add_argument("--evaluations",  type=int,   default=10000, help="Počet vyhodnocení fitness funkce (výchozí: 10000)")
    parser.add_argument("--theta",        type=float, default=0.002, help="Parametr theta algoritmu QIGA (výchozí: 0,002)")
    parser.add_argument("--c1",           type=float, default=0.5,   help="Kognitivní koeficient algoritmu QIPSO (výchozí: 0,05)")
    parser.add_argument("--c2",           type=float, default=0.25,  help="Sociální koeficient algoritmu QIPSO (výchozí: 0,25)")
    parser.add_argument("--omega",        type=float, default=0.01,  help="Parametr omega algoritmu QIPSO (výchozí: 0,01)")
    parser.add_argument("--velocity",     type=float, default=None,  help="Počáteční rychlost algoritmů QIPSO (výchozí: 100) a QSE (výchozí: 1)")
    parser.add_argument("--cooling_rate", type=float, default=0.98,  help="Míra chlazení algoritmu QISA (výchozí: 0,98)")
    parser.add_argument("--cooling",      choices=cooling,     default="rec-logarithmic", help="Chladící plán algoritmu QISA (výchozí: rec-logarithmic)")
    parser.add_argument("--observation",  choices=observation, default="sigmoid",         help="Tepelně-řízené pozorování algoritmu QISA (výchozí: sigmoid)")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = argument_parser()

    generations = calculate_iterations(args.evaluations, args.population)
    print(f"Evaluace: {args.evaluations}, velikost populace: {args.population}, počet generací: {generations}")

    profits, weights, capacity, dataset = load_knapsack_data(args.input)

    results = []
    for i in range(args.experiments):
        if args.algorithm == "qiga":
            fitness, chromosome, fitness_history = qiga (
                item_values       = profits, 
                item_weights      = weights, 
                knapsack_capacity = capacity, 
                population_size   = args.population, 
                num_generations   = generations, 
                theta             = args.theta
            )
        elif args.algorithm == "qisa":
            if args.cooling == "logarithmic" or args.cooling == "rec-logarithmic":
                args.cooling_rate = None
            fitness, chromosome, fitness_history = qisa(
                item_values       = profits, 
                item_weights      = weights, 
                knapsack_capacity = capacity, 
                population_size   = args.population, 
                num_generations   = generations,
                cooling_rate      = args.cooling_rate,
                observation       = args.observation,
                cooling           = args.cooling
            )
        elif args.algorithm == "qse":
            if args.velocity is None:
                args.velocity = 1.0
            fitness, chromosome, fitness_history = qse(
                item_values        = profits, 
                item_weights       = weights, 
                knapsack_capacity  = capacity, 
                population_size    = args.population, 
                num_generations    = generations,
                velocity           = args.velocity
            )
        elif args.algorithm == "qipso":
            if args.velocity is None:
                args.velocity = 100.0
            fitness, chromosome, fitness_history = qipso(
                item_values        = profits, 
                item_weights       = weights, 
                knapsack_capacity  = capacity, 
                population_size    = args.population, 
                num_generations    = generations,
                cognitive          = args.c1,
                social             = args.c2,
                omega              = args.omega,
                velocity           = args.velocity
            )
        
        results.append({"fitness": fitness, "chromosome": chromosome, "fitness_history": fitness_history})

        print(f"Experiment {i + 1}/{args.experiments}: nejlepší hodnota = {fitness}")

    if not args.output:
        exit(0)

    if args.algorithm == "qiga":
        save_results(
            algorithm    = args.algorithm,
            dataset_name = dataset,
            results      = results,
            output_dir   = args.output,
            append       = args.append_results,
            population   = args.population,
            evaluations  = args.evaluations,
            generations  = generations,
            theta        = args.theta
        )

    if args.algorithm == "qisa":
        save_results(
            algorithm    = args.algorithm,
            dataset_name = dataset,
            results      = results,
            output_dir   = args.output,
            append       = args.append_results,
            population   = args.population,
            evaluations  = args.evaluations,
            generations  = generations,
            cooling      = args.cooling,
            cooling_rate = args.cooling_rate,
            observation  = args.observation
        )

    if args.algorithm == "qse":
        save_results(
            algorithm    = args.algorithm,
            dataset_name = dataset,
            results      = results,
            output_dir   = args.output,
            append       = args.append_results,
            population   = args.population,
            evaluations  = args.evaluations,
            generations  = generations,
            velocity     = args.velocity
        )

    if args.algorithm == "qipso":
        save_results(
            algorithm    = args.algorithm,
            dataset_name = args.input,
            results      = results,
            output_dir   = args.output,
            append       = args.append_results,
            population   = args.population,
            evaluations  = args.evaluations,
            generations  = generations,
            c1           = args.c1,
            c2           = args.c2,
            omega        = args.omega,
            velocity     = args.velocity
        )

    
