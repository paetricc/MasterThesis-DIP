######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_utils.py             
# Popis:
# Soubor obsahující pomocné funkce
# pro generování grafů
######################################

import matplotlib.pyplot as plt
import pandas as pd


def plot_optimum(optimum_value: float, label: str = "optimum", color: str = "red"):
    """
    Funkce pro přidáni horizontální čáry a legendy pro optimum do aktuálního grafu.

    Parameters
    ----------
    optimum_value : float
        Hodnota optima.
    label : str
        Text legendy.
    color : str
        Barva čáry.
    """
    plt.axhline(y=optimum_value, color=color, linestyle='--', linewidth=1, label=label)
    plt.legend(fontsize=11)


def filter_df(df, **filters):
    for column, values in filters.items():
        if column in df.columns:
            df = df[df[column].isin(values)]
    return df


def get_filters_best():
    return {
        "algorithm": ["qiga", "qipso", "qse", "qisa"],
        "theta": [0.002],
        "cognitive": [0.5],
        "social": [0.25],
        "omega": [0.01],
        "cooling": ["rec-logarithmic"],
        "observation": ["sigmoid"]
    }
    