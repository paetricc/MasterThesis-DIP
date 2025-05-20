######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: run_plots.py             
# Popis:
# Vstupní bod pro generování grafů
# ze získaných dat pomocí provedených
# experimentů.
######################################

import argparse
import pandas as pd

from itertools import chain
from plots.plot_qiea import *
from plots.utils.futils import load_results, get_algos, create_subdir
from plots.utils.putils import print_algos
from plots.utils.plot_utils import filter_df, get_filters_best


def parse_arguments():
    """
    Funkce pro zpracování argumentů příkazové řádky

    Returns
    -------
    argparse.Namespace : 
        Zpracované argumenty zadané uživatelem
    """
    parser = argparse.ArgumentParser(description="Vykreslení grafů pro evoluční algoritmy a kvantově inspirované evoluční algoritmy.")
    parser.add_argument("source_dir", type=str, help="Cesta ke zdrojové složce (výchozí: outputs)")
    parser.add_argument("--save_dir", type=str, default=None, help="Cesta pro uložení grafů (pokud není zadána, grafy se zobrazí)")
    parser.add_argument("--algorithm", nargs='+', choices=["qiga", "qisa", "qse", "qipso"], default=None, help="Typ algoritmu pro vykreslení.")
    parser.add_argument("--instance", nargs='+', default=None, help="Velikost instance problému pro zpracování.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    available_algorithms = get_algos(args.source_dir)
    print_algos(available_algorithms)

    for algorithm, instances in available_algorithms.items():
        if args.algorithm is not None and algorithm not in args.algorithm: 
            continue
        for instance in instances:
            if args.instance is not None and instance not in args.instance:
                continue
            print(f"Načítání dat pro {algorithm.upper()} s instancí {instance}...")
            data = load_results(args.source_dir, [algorithm], [int(instance)], True)

            if data.empty:
                print(f"Žádná nalezená data pro {algorithm} a jeho instanci {instance}.")

            print(f"Generování grafů pro {algorithm.upper()} a instanci {instance}")
            print("========================================")
            if (algorithm == "qiga"):
                for eval_count in data["evaluations"].unique():
                    print(f"- Počet vyhodnocení fitness funkce: {eval_count}")
                    filtered = data[data["evaluations"] == eval_count]
                    save_subdir = create_subdir(args.save_dir, f"eval_{eval_count}")
                    plot_qiga(filtered, algorithm=algorithm, instance=instance, save_dir=save_subdir)

            if (algorithm == "qisa"):
                for eval_count in data["evaluations"].unique():
                    print(f"- Počet vyhodnocení fitness funkce: {eval_count}")
                    filtered = data[data["evaluations"] == eval_count]
                    save_subdir = create_subdir(args.save_dir, f"eval_{eval_count}")
                    plot_qisa(filtered, algorithm=algorithm, instance=instance, save_dir=save_subdir)

            if (algorithm == "qse"):
                for eval_count in data["evaluations"].unique():
                    print(f"- Počet vyhodnocení fitness funkce: {eval_count}")
                    filtered = data[data["evaluations"] == eval_count]
                    save_subdir = create_subdir(args.save_dir, f"eval_{eval_count}")
                    plot_qse(filtered, algorithm=algorithm, instance=instance, save_dir=save_subdir)

            if (algorithm == "qipso"):
                for eval_count in data["evaluations"].unique():
                    print(f"- Počet vyhodnocení fitness funkce: {eval_count}")
                    filtered = data[data["evaluations"] == eval_count]
                    save_subdir = create_subdir(args.save_dir, f"eval_{eval_count}")
                    plot_qipso(filtered, algorithm=algorithm, instance=instance, save_dir=save_subdir)

    best_results_df = pd.DataFrame()
    for instance in set(chain.from_iterable(available_algorithms.values())):
        if args.instance is not None and instance not in args.instance:
            continue

        for algorithm, instances in available_algorithms.items():
            data = load_results(args.source_dir, instances=[instance], algorithms=[algorithm], load_fitness_history=False)
            filters = get_filters_best()
            best_filtered_results = filter_df(data, **filters)
            best_results_df = pd.concat([best_results_df, best_filtered_results], ignore_index=True)

        for eval_count in best_results_df["evaluations"].unique():
            save_subdir = create_subdir(args.save_dir, f"eval_{eval_count}")
            best_df = best_results_df[best_results_df["evaluations"] == eval_count]

            if args.algorithm is None:
                filtered_qiea_df = best_df[
                    ((best_df["algorithm"] == "qiga")) | ((best_df["algorithm"] == "qisa")) |
                    ((best_df["algorithm"] == "qipso") & best_df["velocity"].isin([100])) |
                    ((best_df["algorithm"] == "qse") & best_df["velocity"].isin([1]))
                ]
                plot_boxplots_best_qiea(filtered_qiea_df, instance, save_dir=save_subdir)

    print("\nVšechny grafy byly úspěšně vygenerovány.")
