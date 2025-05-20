######################################
# Autor: Tomáš Bártů
# Email: xbartu11@stud.fit.vutbr.cz
# Soubor: putils.py             
# Popis:
# Soubor obsahující funkce, jenž 
# slouží k výpisu informací na 
# standardní výstup.
######################################


def print_algos(algorithms):
    """
    Funkce pro výpis nalezených algoritmů a instancí ve zdrojové složce

    Parameters
    ----------
    algorithms : dict[str, list[str]]
        Slovník algoritmů a odpovídajících velikostí instancí
    """
    print("Dostupné algoritmy a jejich instance:")
    print("=====================================")
    max_len = max(len(algo) for algo in algorithms)
    for algo, inst in algorithms.items():
        print(f"{algo.upper().ljust(max_len)} : {', '.join(inst)}")
    print("=====================================")
