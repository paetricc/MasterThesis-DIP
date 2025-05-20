######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_qiea.py             
# Popis:
# Soubor obsahující různé funkce pro 
# vykreslení grafů algoritmů QIEA
######################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from plots.plot_qiga import *
from plots.plot_qisa import *
from plots.plot_qse import *
from plots.plot_qipso import *
from plots.utils.futils import save_plot, create_subdir


def plot_qiga(data: pd.DataFrame, algorithm: str = None, instance: int = 0, save_dir: str = None):
    """
    Funkce pro vykreslení různých grafů algoritmu QIGA:

    Parameters:
        data : pd.DataFrame
            Načtená data.
        algorithm : str
            Název algoritmu.
        instance : int
            Velikost instance problému.
        save_dir : str
            Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(save_dir, algorithm), str(instance))
    
    for popsize in data["population"].unique():
        plot_boxplot_qiga_population(data, instance=instance, population=popsize, save_dir=save_subdir)

    for theta in data["theta"].unique():
        plot_boxplot_qiga_theta(data, instance=instance, theta=theta, save_dir=save_subdir)

    for theta in data["theta"].unique():
        for popsize in data["population"].unique():
            plot_convergence_qiga(data, instance, theta, popsize, save_subdir)
    
    if int(instance) == 100:
        excluded_theta_values = [0.2, 0.5, 1.0, 2.0]
        data = data[~data["theta"].isin(excluded_theta_values)]

    plot_boxplot_qiga_all_theta(data, instance, save_subdir)


def plot_qisa(data: pd.DataFrame, algorithm: str = None, instance: int = 0, save_dir: str = None):
    """
    Funkce pro vykreslení různých grafů algoritmu QISA:

    Parameters:
        data : pd.DataFrame
            Načtená data.
        algorithm : str
            Název algoritmu.
        instance : int
            Velikost instance problému.
        save_dir : str
            Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(save_dir, algorithm), str(instance))

    for cooling in data["cooling"].unique():
        plot_boxplot_qisa_cooling(data, instance, cooling, save_subdir)
    
    for observation in data["observation"].unique():
        plot_boxplot_qisa_observation(data, instance, observation, save_subdir)

    if "cooling_rate" in data.columns:
        for cooling_rate in data["cooling_rate"].unique():
            plot_boxplot_qisa_coolingrate(data, instance, cooling_rate, save_subdir)

    for pop in data["population"].unique():
        plot_boxplot_qisa_col_rate(data[data["cooling"].isin(["linear", "exponential"])], pop, instance, save_subdir)

    for pop in data["population"].unique():
        plot_boxplot_qisa_noncol_rate(data[data["cooling"].isin(["logarithmic", "rec-logarithmic"])], pop, instance, save_subdir)

    for pop in data["population"].unique():
        for observation in data["observation"].unique():
            for cooling in data["cooling"].unique():
                plot_convergence_qisa_noncol_rate(data[data["cooling"].isin(["logarithmic", "rec-logarithmic"])], instance, cooling, observation, pop, save_subdir)
                if "cooling_rate" in data.columns:
                    for cooling_rate in data["cooling_rate"].unique():
                        plot_convergence_qisa_col_rate(data[data["cooling"].isin(["linear", "exponential"])], instance, cooling, cooling_rate, observation, pop, save_subdir)

    for pop in data["population"].unique():
        for observation in data["observation"].unique():
            for cooling in data["cooling"].unique():
                if int(instance) >= 1000:
                    plot_boxplot_qisa_large(data[data["cooling"].isin(["logarithmic", "rec-logarithmic"])], instance, cooling, observation, pop, save_subdir)


def plot_qse(data: pd.DataFrame, algorithm: str = None, instance: int = 0, save_dir: str = None):
    """
    Funkce pro vykreslení různých grafů algoritmu QSE: 

    Parameters:
        data : pd.DataFrame
            Načtená data.
        algorithm : str
            Název algoritmu.
        instance : int
            Velikost instance problému.
        save_dir : str
            Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(save_dir, algorithm), str(instance))

    for pop in data["population"].unique():
        for velocity in data["velocity"].unique():
            if int(instance) >= 1000:
                plot_boxplot_qse_large(data, instance, velocity, pop, save_subdir)
            plot_convergence_qse(data, instance, velocity, pop, save_subdir)


    plot_boxplot_qse_velocity(data, instance, save_subdir)

    excluded_theta_values = [0.0, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0]
    filtered = data[~data["velocity"].isin(excluded_theta_values)]
    plot_boxplot_qse_velocity(filtered, instance, save_subdir, True)
    

def plot_qipso(data: pd.DataFrame, algorithm: str = None, instance: int = 0, save_dir: str = None):
    """
    Funkce pro vykreslení různých grafů algoritmu QIPSO:

    Parameters:
        data : pd.DataFrame
            Načtená data.
        algorithm : str
            Název algoritmu.
        instance : int
            Velikost instance problému.
        save_dir : str
            Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(create_subdir(save_dir, algorithm), str(instance))

    for pop in data["population"].unique():
        for cognitive in data["cognitive"].unique():
            for social in data["social"].unique():
                for omega in data["omega"].unique():
                    for velocity in data["velocity"].unique():
                        if int(instance) >= 1000:
                            plot_boxplot_qipso_large(data, instance, cognitive, social, omega, velocity, pop, save_subdir)
                            plot_convergence_qipso(data, instance, cognitive, social, omega, velocity, pop, save_subdir, False)
                        plot_convergence_qipso(data, instance, cognitive, social, omega, velocity, pop, save_subdir)

    if int(instance) == 100:
        plot_boxplot_qipso_all_omega(data, instance, save_subdir)

    excluded_pop_values = [1, 50, 100]
    data = data[~data["population"].isin(excluded_pop_values)]

    if int(instance) != 100:
        plot_boxplot_qipso_all_omega(data, instance, save_subdir)

    plot_boxplot_qipso_all_velocity(data, instance, save_subdir)    
    plot_boxplot_qipso_all_social(data, instance, save_subdir)
    plot_boxplot_qipso_all_cognition(data, instance, save_subdir)


def plot_boxplots_best_qiea(data: pd.DataFrame, instance: int = 0, save_dir: str = None):
    """
    Funkce pro vykreslení porovnávacích grafů QIEA algoritmů:

    Parameters:
        data : pd.DataFrame
            Načtená data.
        instance : int
            Velikost instance problému.
        save_dir : str
            Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(save_dir, "best")

    sns.set_style("whitegrid")
    
    full_df = data[(data["instance"] == instance)]
    existing_populations = sorted(full_df["population"].unique())
    existing_algorithms = sorted(full_df["algorithm"].unique())

    plt.figure(figsize=(5, 4))
    ax = sns.boxplot(data=full_df, x="population", y="fitness", hue="algorithm",
                     palette="pastel", dodge=True, linewidth=2, order=existing_populations, hue_order=existing_algorithms)
    plt.title(f"Srovnání kvantově inspirovaných evolučních\nalgoritmů při velikosti instance {instance}")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.tight_layout()
    save_plot(save_subdir, f"best_all_qiea_{instance}.pdf")
    plt.close()
