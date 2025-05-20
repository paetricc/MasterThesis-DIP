######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: constants.py             
# Popis:
# Soubor obsahující pomocné funkce, 
# jež pracují se soubory
######################################

import os
import pandas as pd
import matplotlib.pyplot as plt

from plots.utils.constants import PARAM_MAP


def get_algos(output_dir: str):
    """
    Funkce pro identifikaci dostupných algoritmů a instancí 
    na základě názvů CSV souborů nacházejících se ve 
    vstupní složce

    Parameters
    ----------
    dir_path : str
        Cesta ke složce obsahující CSV soubory ve formátu 'algoritmus_instance_{parametr:hodnota}*.csv'.

    Return
    ------
    dict[str, list[str]] : Slovník s názvy algoritmů jako klíči a seřazenými velikostmi instancí jako hodnotami. 
    """
    algorithms = {}

    for file_name in os.listdir(output_dir):
        if not file_name.endswith(".csv"):
            continue

        parts = file_name.replace(".csv", "").split("_")
        if len(parts) < 2:
            continue

        algorithm = parts[0].lower()
        instance = parts[1]

        algorithms.setdefault(algorithm, set()).add(instance)

    if not algorithms:
        print("Chyba: Chybějící jakýkoliv validní soubor ve složce.")
        exit(1)

    return {algorithm: sorted(instances, key=int) for algorithm, instances in algorithms.items()}


def load_results(source_dir: str, algorithms=None, instances=None, load_fitness_history=True) -> pd.DataFrame:
    """
    Načte výsledky experimentů ze souborů v dané složce.

    Parameters
    ----------
    source_dir : str
        Cesta ke složce se soubory.
    algorithms : list[str], optional
        Filtr na názvy algoritmů.
    instances : list[int or str], optional
        Filtr na instance problémů.
    load_fitness_history : bool
        Pokud True, načítá i průběh fitness.

    Returns
    -------
    pd.DataFrame : Výsledky experimentů.
    """
    data = []

    algorithms = set(algorithms) if algorithms else None
    instances = set(map(str, instances)) if instances else None

    for file_name in os.listdir(source_dir):
        if not file_name.endswith(".csv"):
            continue

        params = parse_filename_metadata(file_name)

        if not params:
            continue

        algo = params.get("algorithm")
        inst = params.get("instance")

        if (algorithms and algo not in algorithms) or (instances and inst not in instances):
            continue

        file_path = os.path.join(source_dir, file_name)

        try:
            cols = ["Experiment", "Fitness"]
            if load_fitness_history:
                cols.append("FitnessHistory")
            df = pd.read_csv(file_path, usecols=cols)

            if load_fitness_history:
                df["fitness_history"] = df["FitnessHistory"].apply(lambda x: [float(n) for n in x.split(";")])

            for _, row in df.iterrows():
                entry = {
                    **params,
                    "experiment": row["Experiment"],
                    "fitness": row["Fitness"],
                }
                if load_fitness_history:
                    entry["fitness_history"] = row["fitness_history"]
                data.append(entry)

        except Exception as e:
            print(f"[Chyba] {file_name}: {e}")
            continue

    return pd.DataFrame(data)


def parse_filename_metadata(file_name: str) -> dict:
    """
    Extrahuje parametry algoritmu z názvu CSV souboru.

    Parameters
    ----------
    file_name : str

    Returns
    -------
        dict : obsahuje algorithm, instance a parametry
    """
    params = {}
    parts = file_name.replace(".csv", "").split("_")
    if len(parts) < 2:
        return {}

    params["algorithm"] = parts[0].lower()
    params["instance"] = parts[1]

    for part in parts[1:]:
        if ":" not in part:
            continue
        key, val = part.split(":")
        mapping = PARAM_MAP.get(key)
        if mapping is None:
            continue
        if isinstance(mapping, tuple):
            name, typ = mapping
        else:
            name, typ = key, mapping
        try:
            params[name] = typ(val)
        except ValueError:
            continue

    return params


def create_subdir(base_dir: str, subdir: str) -> str:
    """
    Vytvoří podsložku ve složce a vrátí k ní cestu.

    Parameters
    ----------
    base_dir : str
        Základní složka, do které se má vytvořit podsložka.
    subdir : str 
        Název nové podsložky.

    Returns
    -------
    str : Cesta k vytvořené podsložce nebo None.
    """
    if base_dir is None:
        return None
    subdir = os.path.join(base_dir, subdir)
    os.makedirs(subdir, exist_ok=True)
    return subdir


def save_plot(save_dir: str, filename: str):
    """
    Uloží aktuální graf do zadané složky a souboru, nebo jej 
    zobrazí na obrazovce, pokud složka není zadána.

    Parameters
    ----------
    save_dir : str
        Cílová složka pro uložení grafu. 
        Pokud None, graf se pouze zobrazí.
    filename : str
        Název souboru včetně přípony.
    """
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        output_path = os.path.join(save_dir, filename)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', format=filename.split('.')[-1])
        print(f"Graf byl uložen jako {output_path}")
    else:
        plt.show()


def save_stats(data: pd.DataFrame, save_dir: str, file_name: str, groupby_column, value_column: str):
    """
    Vypočítá základní statistiky pro seskupené hodnoty a uloží je do CSV.

    Parameters
    ----------
    data : pd.DataFrame
        Vstupní data.
    save_dir : str
        Cílová složka pro uložení.
    file_name : str
        Název výsledného CSV souboru.
    groupby_columns : str nebo list[str]
        Jeden nebo více sloupců pro seskupení.
    value_column : str
        Sloupec, pro který se počítají statistiky.
    """
    if not save_dir:
        return

    output_path = os.path.join(save_dir, file_name)

    if isinstance(groupby_column, str):
        groupby = [groupby_column]
    else:
        groupby = groupby_column

    stats = data.groupby(groupby)[value_column].agg(
        mean="mean",
        std="std",
        median="median",
        q25=lambda x: x.quantile(0.25),
        q75=lambda x: x.quantile(0.75),
        max="max",
        count="count"
    ).reset_index()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    stats.to_csv(output_path, index=False)
    print(f"Statistiky byly uloženy jako {output_path}")
