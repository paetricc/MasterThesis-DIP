######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_qse.py             
# Popis:
# Soubor obsahující různé funkce pro 
# vykreslení grafů algoritmu QSE
######################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from plots.utils.futils import save_plot, create_subdir, save_stats
from plots.utils.plot_utils import plot_optimum
from plots.utils.constants import OPT_FITNESS


def plot_convergence_qse(data: pd.DataFrame, instance: int, velocity: float, population: int, save_dir: str = None):
    """
    Vykreslí konvergenční křivku pro danou velikost populace a počáteční rychlost v QSE. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    velocity : float
        Hodnota počáteční rychlosti, pro kterou bude graf vykreslen.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(save_dir, "convergence")

    filtered = data[(data["velocity"] == velocity) & (data["population"] == population)]
    fitness_histories = filtered["fitness_history"].tolist()

    if not fitness_histories:
        print(f"Žádná data pro počáteční rychlost={velocity}, population={population}")
        return

    max_length = max(len(fitness) for fitness in fitness_histories)
    aligned_fitness = np.array([
        np.pad(fitness, (0, max_length - len(fitness)), mode='edge')
        for fitness in fitness_histories
    ])

    median_fitness = np.median(aligned_fitness, axis=0)
    min_fitness = np.min(aligned_fitness, axis=0)
    max_fitness = np.max(aligned_fitness, axis=0)
    Q1 = np.percentile(aligned_fitness, 25, axis=0)
    Q3 = np.percentile(aligned_fitness, 75, axis=0)

    plt.figure(figsize=(7, 4))
    plt.fill_between(range(max_length), min_fitness, max_fitness, color='lightblue', alpha=0.5, label='min-max')
    plt.fill_between(range(max_length), Q1, Q3, color='blue', alpha=0.4, label='Q1-Q3')
    plt.plot(median_fitness, color='black', label='medián')

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.xscale("log")
    plt.xlabel("Generace (log)")
    plt.ylabel("Fitness")
    plt.title(f"Počáteční rychlost: {velocity} a populace {population} (QSE-{instance})")
    plt.legend()
    plt.grid(True)
    save_plot(save_subdir, f"qse_convergence_{instance}_velocity_{velocity}_population_{population}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qse_{instance}_velocity_{velocity}_population_{population}.csv", groupby_column=["velocity", "population"], value_column="fitness")



def plot_boxplot_qse_velocity(data: pd.DataFrame, instance: int, save_dir: str = None, filtered: bool = False):
    """
    Vykreslí krabicové grafy pro všechny velikosti populací a počáteční rychlosti v QSE. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    save_dir : str
        Cílová složka pro uložení grafu.
    filtered : bool
        Pokud jsou data filtrovana vykreslí se i body
    """
    save_subdir = create_subdir(save_dir, str("velocity"))

    if not filtered:
        sns.boxplot(data=data, x="population", y="fitness", hue="velocity", palette="Set3", dodge=True)
    else:
        sns.boxplot(data=data, x="population", y="fitness", hue="velocity", palette="Set3", dodge=True)
        sns.stripplot(data=data, x="population", y="fitness", color="grey", size=3)
    plt.title(f"Vliv počáteční rychlosti a velikosti populace (QSE-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title=f"Počáteční\nrychlost", loc="lower right")
    if not filtered:
        save_plot(save_subdir, f"boxplot_qse_{instance}_velocity.pdf")
    else:
        save_plot(save_subdir, f"boxplot_qse_{instance}_velocity_filtered.pdf")
    plt.close()


def plot_boxplot_qse_large(data: pd.DataFrame, instance: int, velocity: str, population: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro vetší instance problému a vybranou velikost populace a počáteční rychlost v QSE. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    velocity : float
        Hodnota počáteční rychlosti, pro kterou bude graf vykreslen.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(save_dir, "summary")

    filtered = data[(data["velocity"] == velocity) & (data["population"] == population)]

    plt.figure(figsize=(4, 8))
    sns.boxplot(data=filtered, x="population", y="fitness", hue="velocity", palette="Set3", legend=False)
    sns.stripplot(data=filtered, x="population", y="fitness", color="grey", size=3)
    plt.title(f"Počáteční rychlost: {velocity}\n (QSE-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(loc="upper right")    
    save_plot(save_subdir, f"boxplot_qse_{instance}_large.pdf")
    plt.close()
