######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_qiga.py             
# Popis:
# Soubor obsahující různé funkce pro 
# vykreslení grafů algoritmu QIGA
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


def plot_boxplot_qiga_population(data: pd.DataFrame, population: int, instance: int, save_dir: str = None):
    """
    Vykreslí boxplot fitness hodnot pro danou velikost populace v QIGA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    instance : int
        Velikost instance problému.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """
    save_subdir = create_subdir(save_dir, str("population"))

    filtered = data[data["population"] == population]
    
    sns.boxplot(data=filtered, x="theta", y="fitness", hue="theta", palette="Set3", dodge=False, legend=False)
    sns.stripplot(data=filtered, x="theta", y="fitness", color="grey", size=2)
    plt.title(f"Velikost populace {population} (QIGA-{instance})")
    plt.xlabel("Parametr $\Delta \\theta$")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    save_plot(save_subdir, f"boxplot_qiga_{instance}_popsize_{population}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qiga_{instance}_popsize_{population}.csv", groupby_column="theta", value_column="fitness")


def plot_boxplot_qiga_theta(data: pd.DataFrame, theta: float, instance: int, save_dir: str = None):
    """
    Vykreslí boxplot fitness hodnot pro danou hodnotu theta v QIGA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    theta : float
        Hodnota parametru theta, pro který bude graf vykreslen.
    instance : int
        Velikost instance problému.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """
    save_subdir = create_subdir(save_dir, str("theta"))

    filtered = data[data["theta"] == theta]

    if int(instance) >= 1000:
        plt.figure(figsize=(4, 8))

    sns.boxplot(data=filtered, x="population", y="fitness", hue="population", palette="Set3", dodge=False, legend=False)
    sns.stripplot(data=filtered, x="population", y="fitness", color="grey", size=3)
    plt.title(f"Parametr $\Delta \\theta$: {theta} (QIGA-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    if int(instance) >= 1000:
        plt.title(f"$\Delta \\theta$: {theta} (QIGA-{instance})")
        plt.legend(loc='upper right')
    
    save_plot(save_subdir, f"boxplot_qiga_{instance}_theta_{theta}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qiga_{instance}_theta_{theta}.csv", groupby_column="theta", value_column="fitness")


def plot_convergence_qiga(data: pd.DataFrame, instance: int, theta: float, population: int, save_dir: str = None):
    """
    Vykreslí konvergenční křivku pro danou velikost populace a parametr theta v QIGA. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    theta : float
        Hodnota parametru theta, pro který bude graf vykreslen.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str, optional
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(save_dir, "convergence")

    filtered = data[(data["theta"] == theta) & (data["population"] == population)]
    fitness_histories = filtered["fitness_history"].tolist()

    if not fitness_histories:
        print(f"Žádná data pro theta={theta}, population={population}")
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
    plt.title(f"Parametr $\Delta \\theta$: {theta} a populace {population} (QIGA-{instance})")
    plt.legend()
    plt.grid(True)
    save_plot(save_subdir, f"qiga_convergence_{instance}_theta_{theta}_population_{population}.pdf")
    plt.close()


def plot_boxplot_qiga_all_theta(data: pd.DataFrame, instance: int, save_dir: str = None):
    """
    Vykreslí boxplot fitness hodnot pro všechny hodnoty theta a velikosti populace v QIGA.

    Zobrazuje rozložení fitness podle velikosti populace a parametrů theta.
    Pokud je známo optimum pro danou instanci, přidá ho jako referenční čáru.
    Výsledný graf a agregované statistiky jsou uloženy do zadané složky.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """
    save_subdir = create_subdir(create_subdir(create_subdir(save_dir, str("all")), str(instance)), str("qiga"))

    if int(instance) >= 1000:
        plt.figure(figsize=(5, 8))

    sns.boxplot(data=data, x="population", y="fitness", hue="theta", palette="Set3", dodge=True, legend=True)
    plt.title(f"Vliv parametru $\Delta \\theta$ a velikosti populace (QIGA-{instance})")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title="$\Delta \\theta$", ncol=2)
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")
    save_plot(save_subdir, f"boxplot_qiga_{instance}_all_theta.pdf")
    plt.close()

    save_stats(data, save_subdir, f"stats_qiga_{instance}_all_theta.csv", groupby_column="theta", value_column="fitness")
