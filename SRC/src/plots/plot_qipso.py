######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_qipso.py             
# Popis:
# Soubor obsahující různé funkce pro 
# vykreslení grafů algoritmu QIPSO
######################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from plots.utils.futils import save_plot, create_subdir, save_stats
from plots.utils.plot_utils import plot_optimum
from plots.utils.constants import OPT_FITNESS
from plots.utils.plot_config import set_plot_style
set_plot_style()


def plot_convergence_qipso(data: pd.DataFrame, instance: int, cognitive: float, social: float, omega: float, velocity: str, population: int, save_dir: str = None, log=True):
    """
    Vykreslí konvergenční křivku pro danou velikost populace, parametr omega 
    kognitivní koeficient, sociální koeficient a počáteční rychlost v QIPSO. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    cognitive : float
        Kognitivní koeficient.
    social : float
        Sociální koeficient.
    omega : float
        Parametr omega.
    velocity : float
        Hodnota počáteční rychlosti, pro kterou bude graf vykreslen.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str
        Cílová složka pro uložení grafu.
    log : bool
        Zda má být x-ová osa logaritmická.
    """
    save_subdir = create_subdir(save_dir, "convergence")

    filtered = data[(data["velocity"] == velocity) & (data["population"] == population) & (data["cognitive"] == cognitive) & (data["social"] == social) & (data["omega"] == omega)]
    fitness_histories = filtered["fitness_history"].tolist()

    if not fitness_histories:
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

    if log:
        plt.xscale("log")
        plt.xlabel("Generace (log)")
    else:
        plt.xlabel("Generace")
    plt.ylabel("Fitness")
    plt.title(f"Počáteční rychlost: {velocity}, $c_1$: {cognitive}, $c_2$: {cognitive},\n$\omega$: {omega} a populace {population} (QIPSO-{instance})")
    plt.legend()
    plt.grid(True)
    if log:
        save_plot(save_subdir, f"qipso_convergence_{instance}_c1_{cognitive}_c2_{social}_omega_{omega}_velocity_{velocity}_population_{population}.pdf")
    else:
        save_plot(save_subdir, f"qipso_convergence_nonlog_{instance}_c1_{cognitive}_c2_{social}_omega_{omega}_velocity_{velocity}_population_{population}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qipso_{instance}_c1_{cognitive}_c2_{social}_omega_{omega}_velocity_{velocity}_population_{population}.csv", groupby_column=["velocity", "population", "cognitive", "social", "omega"], value_column="fitness")


def plot_boxplot_qipso_large(data: pd.DataFrame, instance: int, cognitive: float, social: float, omega: float, velocity: str, population: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro větší instance pro danou velikost populace, parametr omega 
    kognitivní koeficient, sociální koeficient a počáteční rychlost v QIPSO. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    cognitive : float
        Kognitivní koeficient.
    social : float
        Sociální koeficient.
    omega : float
        Parametr omega.
    velocity : float
        Hodnota počáteční rychlosti, pro kterou bude graf vykreslen.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(save_dir, "summary")

    filtered = data[(data["velocity"] == velocity) & (data["population"] == population) & (data["cognitive"] == cognitive) & (data["social"] == social) & (data["omega"] == omega)]

    plt.figure(figsize=(4, 8))
    sns.boxplot(data=filtered, x="population", y="fitness", hue="velocity", palette="Set3", legend=False)
    sns.stripplot(data=filtered, x="population", y="fitness", color="grey", size=3)
    plt.title(f"Počáteční rychlost: {velocity},\n $c_1$: {cognitive}, $c_2$: {social}, $\omega$: {omega}\n(QIPSO-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(loc="upper right")    
    save_plot(save_subdir, f"boxplot_qipso_{instance}_large_{velocity}.pdf")
    plt.close()


def plot_boxplot_qipso_all_cognition(data: pd.DataFrame, instance: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro všechny velikosti populací a kognitivní koeficient v QIPSO.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(create_subdir(save_dir, str("all")), str(instance)), str("qipso"))

    sns.boxplot(data=data, x="population", y="fitness", hue="cognitive", palette="Set3", dodge=True)
    plt.title(f"Vliv kognitivního koeficientu a velikosti populace (QIPSO-{instance})")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])
    
    plt.legend(title="Kognitivní\nkoeficient")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")
    save_plot(save_subdir, f"boxplot_qipso_{instance}_all_cognitive.pdf")
    plt.close()    


def plot_boxplot_qipso_all_social(data: pd.DataFrame, instance: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro všechny velikosti populací a sociální koeficient v QIPSO.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(create_subdir(save_dir, str("all")), str(instance)), str("qipso"))

    sns.boxplot(data=data, x="population", y="fitness", hue="social", palette="Set3", dodge=True)
    plt.title(f"Vliv sociálního koeficientu a velikosti populace (QIPSO-{instance})")

    
    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title="Sociální\nkoeficient")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")
    save_plot(save_subdir, f"boxplot_qipso_{instance}_all_social.pdf")
    plt.close()


def plot_boxplot_qipso_all_omega(data: pd.DataFrame, instance: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro všechny velikosti populací a parametry omega v QIPSO.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(create_subdir(save_dir, str("all")), str(instance)), str("qipso"))

    sns.boxplot(data=data, x="population", y="fitness", hue="omega", palette="Set3", dodge=True)
    plt.title(f"Vliv parametru $\omega$ a velikosti populace (QIPSO-{instance})")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title="$\omega$")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")
    save_plot(save_subdir, f"boxplot_qipso_{instance}_all_omega.pdf")
    plt.close()


def plot_boxplot_qipso_all_velocity(results_df: pd.DataFrame, instance: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro všechny velikosti populací a počáteční rychlosti v QIPSO.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    save_dir : str
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(create_subdir(save_dir, str("all")), str(instance)), str("qipso"))

    sns.boxplot(data=results_df, x="population", y="fitness", hue="velocity", palette="Set3", dodge=True)
    plt.title(f"Vliv počáteční rychlosti a velikosti populace (QIPSO-{instance})")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title="Počáteční rychlost", ncol=2)
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")
    save_plot(save_subdir, f"boxplot_qipso_{instance}_all_velocity.pdf")
    plt.close()
