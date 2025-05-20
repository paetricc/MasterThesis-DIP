######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: plot_config.py             
# Popis:
# Soubor sloužící k nastavení 
# základních vlastností grafů
######################################

import matplotlib.pyplot as plt


def set_plot_style():
    """
    Funkce pro nastavení globálního stylu grafů.
    """
    plt.rcParams.update({
        "font.size": 12,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "figure.figsize": (7.5, 5),
        "savefig.bbox": "tight",
    })
