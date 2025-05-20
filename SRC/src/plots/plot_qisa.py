######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_qisa.py             
# Popis:
# Soubor obsahující různé funkce pro 
# vykreslení grafů algoritmu QISA
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


def plot_boxplot_qisa_cooling(data: pd.DataFrame, instance: int, cooling: str, save_dir: str = None):
    """
    Vykreslí boxplot fitness hodnot pro danou hodnotu chladicího plánu v QISA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    cooling : str
        Zvolený chladicí plán, pro který bude graf vykreslen.
    instance : int
        Velikost instance problému.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """
    save_subdir = create_subdir(save_dir, str("cooling"))
    
    filtered = data[data["cooling"] == cooling]

    if int(instance) >= 1000:
        plt.figure(figsize=(4, 8))

    if "cooling_rate" in filtered.columns and filtered["cooling_rate"].nunique(dropna=True) > 1:
        sns.boxplot(data=filtered, x="population", y="fitness", hue="cooling_rate", palette="Set3")
    else:
        sns.boxplot(data=filtered, x="population", y="fitness", hue="population", palette="Set3")

    plt.title(f"Chladicí plán: $\mathit{{{cooling}}}$ (QISA-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")
    
    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title="Míra ochlazování")
    save_plot(save_subdir, f"boxplot_qisa_{instance}_cooling_{cooling}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qisa_{instance}_cooling_{cooling}.csv", groupby_column="cooling", value_column="fitness")


def plot_boxplot_qisa_observation(data: pd.DataFrame, instance: int, heated: str, save_dir: str = None):
    """
    Vykreslí boxplot fitness hodnot pro danou hodnotu zahřívací funkce v QISA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    heated : str
        Zvolená zahřívací funkce, pro který bude graf vykreslen.
    instance : int
        Velikost instance problému.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """
    save_subdir = create_subdir(save_dir, str("heated"))
    
    filtered = data[data["observation"] == heated]

    if int(instance) >= 1000:
        plt.figure(figsize=(4, 8))

    sns.boxplot(data=filtered, x="population", y="fitness", hue="cooling", palette="Set3")
    plt.title(f"Zahřívací funkce: $\mathit{{{heated}}}$ (QISA-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])
    
    plt.legend(title="Chladicí plán")
    save_plot(save_subdir, f"boxplot_qisa_{instance}_heated_{heated}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qisa_{instance}_heated_{heated}.csv", groupby_column="observation", value_column="fitness")


def plot_boxplot_qisa_coolingrate(data: pd.DataFrame, instance: int, coolingrate: float, save_dir: str = None):
    """
    Vykreslí boxplot fitness hodnot pro danou míru ochlazování v QISA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    coolingrate : int
        Zvolená míra ochlazování, pro který bude graf vykreslen.
    instance : int
        Velikost instance problému.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """    
    save_subdir = create_subdir(save_dir, str("cooling_rate"))
    
    filtered = data[data["cooling_rate"] == coolingrate]

    if int(instance) >= 1000:
        plt.figure(figsize=(4, 8))

    sns.boxplot(data=filtered, x="population", y="fitness", hue="cooling", palette="Set3")
    plt.title(f"Míra ochlazování: $\mathit{{{coolingrate}}}$ (QISA-{instance})")
    plt.xlabel("Velikost populace")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])
    
    plt.legend(title="Chladicí plán")
    save_plot(save_subdir, f"boxplot_qisa_{instance}_cooling-rate_{coolingrate}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qisa_{instance}_cooling-rate_{coolingrate}.csv", groupby_column="cooling_rate", value_column="fitness")


def plot_boxplot_qisa_col_rate(data: pd.DataFrame, population: int, instance: int, save_dir: str = None):
    """
    Vykreslí catplot fitness hodnot pro danou populaci a všechny chladicí plány, které využívají míru chlazení v QISA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """ 
    if data.empty:
        return
    
    save_subdir = create_subdir(save_dir, str("cooling_cooling-rate"))

    filtered = data[data["population"] == population]

    g = sns.catplot(
        data=filtered,
        x="observation",
        y="fitness",
        hue="cooling_rate",
        col="cooling",
        kind="box",
        palette="Set3",
        height=4,
        col_wrap=2,
    )

    g.set_titles(col_template="Chladicí plán: {col_name}", row_template="Zahřívací funkce: {row_name}")
    g.set_axis_labels("", "Fitness")
    if g._legend:
        g._legend.remove()
    g.add_legend(title="Míra ochlazování", bbox_to_anchor=(0.98, 0.2), ncol=2)

    optimum_value = OPT_FITNESS[int(instance)]
    for ax in g.axes.flatten():
        ax.axhline(y=optimum_value, color="red", linestyle="--", linewidth=1, label="Optimum")
        ax.yaxis.grid(True)

    g.figure.suptitle(f"Populace: {population} (QISA-{instance})")

    save_plot(save_subdir, f"facet_boxplot_qisa_{instance}_population_{population}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qisa_{instance}_population_{population}.csv", groupby_column=["cooling", "observation", "cooling_rate"], value_column="fitness")


def plot_boxplot_qisa_noncol_rate(data: pd.DataFrame, population: int, instance: int, save_dir: str = None):
    """
    Vykreslí catplot fitness hodnot pro danou populaci a všechny chladicí plány, které nevyužívají míru chlazení v QISA. 
    Společně s vykreslením grafu jsou spočteny a statistické charakteristiky dat.

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str, optional
        Cílová složka pro uložení grafu a statistik.
    """ 
    save_subdir = create_subdir(save_dir, str("cooling_non-cooling-rate"))

    filtered = data[data["population"] == population]

    if int(instance) >= 1000:
        plt.figure(figsize=(4, 8))

    plt.figure(figsize=(6, 4))
    sns.boxplot(data=filtered, x="observation", y="fitness", hue="cooling", palette="Set3")
    plt.title(f"Populace: {population} (QISA-{instance})")
    plt.xlabel("Zahřívací funkce")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(title="Chladicí plán")    
    save_plot(save_subdir, f"boxplot_qisa_{instance}_population_{population}.pdf")
    plt.close()

    save_stats(filtered, save_subdir, f"stats_qisa_{instance}_population_{population}.csv", groupby_column=["cooling", "observation"], value_column="fitness")


def plot_convergence_qisa_noncol_rate(data: pd.DataFrame, instance: int, cooling: str, observation: str, population: int, save_dir: str = None):
    """
    Vykreslí konvergenční křivku pro danou populaci, chladící plán a tepelně-řízené pozorování, které nevyužívají míru chlazení v QISA. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    cooling : str
        Zvolený chladicí plán, pro který bude graf vykreslen.
    observation : str
        Zvolené tepelně-řízení pozorování.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str, optional
        Cílová složka pro uložení grafu.
    """ 
    save_subdir = create_subdir(create_subdir(save_dir, "convergence"), "non-cooling-rate")

    filtered = data[(data["cooling"] == cooling) & (data["observation"] == observation) & (data["population"] == population)]
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

    plt.xscale("log")
    plt.xlabel("Generace (log)")
    plt.ylabel("Fitness")
    plt.title(f"Chladicí plán: $\mathit{{{cooling}}}$, zahřívací funkce: $\mathit{{{observation}}}$ \n a populace {population} (QISA-{instance})")
    plt.legend()
    plt.grid(True)
    save_plot(save_subdir, f"qisa_convergence_{instance}_cooling_{cooling}_observation_{observation}_population_{population}.pdf")
    plt.close()


def plot_convergence_qisa_col_rate(data: pd.DataFrame, instance: int, cooling: str, cooling_rate: float, observation: str, population: int, save_dir: str = None):
    """
    Vykreslí konvergenční křivku pro danou populaci, chladící plán, míru chlazení a tepelně-řízené pozorování, které využívají míru chlazení v QISA. 

    Parameters
    ----------
    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    cooling : str
        Zvolený chladicí plán, pro který bude graf vykreslen.
    cooling_rate : float
        Zvolený míra chlazení.
    observation : str
        Zvolené tepelně-řízení pozorování.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str, optional
        Cílová složka pro uložení grafu.
    """ 
    save_subdir = create_subdir(create_subdir(save_dir, "convergence"), "cooling-rate")

    filtered = data[(data["cooling"] == cooling) & (data["cooling_rate"] == cooling_rate) & (data["observation"] == observation) & (data["population"] == population)]
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

    plt.xscale("log")
    plt.xlabel("Generace (log)")
    plt.ylabel("Fitness")
    plt.title(f"Chladicí plán: $\mathit{{{cooling}}}$, míra chlazení: {cooling_rate},\n zahřívací funkce: $\mathit{{{observation}}}$ a populace {population} (QISA-{instance})")
    plt.legend()
    plt.grid(True)
    save_plot(save_subdir, f"qisa_convergence_{instance}_cooling_{cooling}_cooling-rate_{cooling_rate}_observation_{observation}_population_{population}.pdf")
    plt.close()


def plot_boxplot_qisa_large(data: pd.DataFrame, instance: int, cooling: str, observation: str, population: int, save_dir: str = None):
    """
    Vykreslí krabicové grafy pro větší instance pro danou velikost populace, chladící plán a tepelně-řízené pozorován v QISA.

    data : pd.DataFrame
        Data experimentů.
    instance : int
        Velikost instance problému.
    cooling : str
        Zvolený chladicí plán, pro který bude graf vykreslen.
    observation : str
        Zvolené tepelně-řízení pozorování.
    population : int
        Velikost populace, pro kterou bude graf vykreslen.
    save_dir : str, optional
        Cílová složka pro uložení grafu.
    """
    save_subdir = create_subdir(save_dir, "summary")

    filtered = data[(data["cooling"] == cooling) & (data["observation"] == observation) & (data["population"] == population)]

    plt.figure(figsize=(4, 8))
    sns.boxplot(data=filtered, x="observation", y="fitness", hue="cooling", palette="Set3", legend=False)
    sns.stripplot(data=filtered, x="observation", y="fitness", color="grey", size=3)
    plt.title(f"Chladicí plán: $\mathit{{{cooling}}}$\n (QISA-{instance})")
    plt.xlabel("Zahřívací funkce")
    plt.ylabel("Fitness")
    plt.grid(axis="y")

    if int(instance) in OPT_FITNESS:
        plot_optimum(OPT_FITNESS[int(instance)])

    plt.legend(loc="upper right")    
    save_plot(save_subdir, f"boxplot_qisa_{instance}_large.pdf")
    plt.close()
 