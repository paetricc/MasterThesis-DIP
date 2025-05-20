# Kvantově inspirované optimalizační algoritmy

---
* Autor: Tomáš Bártů
* Email: [xbartu11@fit.vutbr.cz](mailto:xbartu11@fit.vutbr.cz)
---

Cílem této diplomové práce je prozkoumat možnosti optimalizačních algoritmů, jež jsou inspirovány principy kvantové fyziky a ověřit jejich praktickou využitelnost na konkrétní úloze, přičemž zde byl vybrán problém batohu ve variantě 0-1.  
Tyto algoritmy, označované jako kvantově inspirované evoluční algoritmy (*Quantum Inspired Evolutionary Algorithms - QIEA*), pracují na klasických výpočetních systémech, ale využívají koncepty jako superpozice stavů nebo pravděpodobnostní reprezentace, čímž rozšiřují tradiční evoluční a heuristické přístupy. 

## Struktura projektu
Níže je popsaná základní struktura projektu společně s vysvětlením, co jednotlivé složky obsahují/neobsahují. 

* `datasets/`: Datové sady pro instance velikosti 100, 250, 500, 1000, 2000, 5000 a 10000.
* `graphs/`: Vygenerované grafy nad daty nacházející se ve složce `outputs/`, přičemž grafy jsou dále strukturovány do podsložek dle názvu algoritmu, velikosti instance a typu vykreslované informace. 
* `outputs/`: Složka obsahující data experimentů, jež byla provedena na větších instancích (1000, 2000, 5000 a 10000) pro počet evaluací 10000 a 100000, jelikož výpočet je časově náročnější. Výsledky experimentů pro menší instance nebyly zahrnuty pro větší přehlednost. 
* `scripts/`: Složka se skripty, které jsou členěny dle názvu algoritmu společně s podsložkou obsahující skripty, jež se spouští na pozadí s nízkou prioritou pro každý nezávislý běh algoritmu. 
* `src/`:
  * `plots/`: Složka obsahující logiku pro vykreslování grafů pro jednotlivé algoritmy. 
    * `utils/`: Složka obsahující soubory s pomocnými funkcemi pro načítaní, zpracování a vykreslení dat. 
  * `qiea/`: Složka obsahující implementace jednotlivých algoritmů společně se souborem zahrnujícím fitness funkce, funkci pro opravu pozorování a různé kvantově inspirované operace. 
  * `plots.py`: Vstupní bod pro generování grafů.
  * `qiea.py`: Vstupní bod pro spouštění jednotlivých algoritmů.
  * `utils.py`: Soubor obsahující pomocné funkce pro načítaní a zpracování dat. 
* `Makefile`: Soubor jimž je možné spouštět skripty a generovat grafy. 

## Algoritmy
Implementace kvantově inspirovaných evolučních algoritmů uvažuje následující algoritmy:
* kvantově inspirovaný genetický algoritmus (*Quantum Inspired Genetic Algorithm - QIGA*),
* kvantově inspirované simulované žíhání (*Quantum Inspired Simulated Annealing - QISA*),
* kvantová evoluce roje (*Quantum Swarm Evolutionary - QSE*) a 
* kvantově inspirovaná optimalizace rojem částic (*Quantum Inspired Particle Swarm Optimization*).

Poslední ze zmíněných algoritmů byl navržen v rámci práce. 
Jedná se o kombinaci algoritmu *QIGA*, jenž využívá kvantové rotační hradlo pro úpravu pravděpodobnostních koeficientů kvantových chromozomů a o kombinaci *QSE*, jenž využívá kolektivní učení v kontextu pohybu částic pomocí určeních jejich rychlostí. 

Navržená implementace využívá kvantové rotační hradlo rovněž pro úpravu pravděpodobnostních koeficientů kvantových chromozomů, ale namísto statické velikosti změny, dynamicky upravuje velikost změny, jež je dána rychlostí částice. 

## Spuštění implementace algoritmů

Nápovědu k parametrizaci jednotlivých algoritmů je možné zobrazit pomocí příkazu:
```bash
python3 src/qiea.py --help
```
přičemž pokaždé musí být při spouštění vybraného algoritmu na vstupu specifikováno po řadě:
* název algoritmu (`qiga`, `qisa`, `qse` nebo `qipso`) a
* cesta k datové sadě.

Nezávisle na názvu algoritmu můžou být vybrány následující parametry:
* `--output`: Cesta k adresáři pro uložení výsledků, kdy v případě jeho nespecifikování nedojde k uložení výsledků do souboru.
* `--experiments`: Počet nezávislých běhů algoritmu.
* `--evaluations`: Počet vyhodnocení fitness funkce.
* `--population`: Počet jedinců v populaci.
* `--append_results`: Přepínač pro připojení výsledků k existujícímu souboru. 

Příklad spuštění experimentů algoritmu *QISA* s výchozím nastavením parametrů na datové sadě `100.txt`:
```bash
python3 src/qiea.py qisa datasets/100.txt
```
a pro specifické nastavení nezávislých parametrů
```bash
python3 src/qiea.py qisa datasets/100.txt --output outputs/ --experiments 5 --evaluations 1000 --population 2
```
Případně je možné ještě použít přepínač `--append_results` pro připojení výsledků do již existujícího souboru. 

### *QIGA*
Kvantově inspirovaný genetický algoritmus má pouze jeden přídavný parametr a to:
* `--theta`: Úhel určující velikost úpravy pravděpodobnostních chromozomů kvantových chromozomů. 

Příklad použití při výchozím nastavení nezávislých parametrů:
```bash
python3 src/qiea.py qiga datasets/100.txt --theta 0.01
```

### *QISA*
Kvantově inspirované simulované žíhání má k dispozici následující přídavné parametry:
* `--cooling_rate`: Určuje míru ochlazování.
* `--cooling`: Specifikuje chladicí plán (`exponential`, `linear`, `logarithmic` nebo `rec-logarithmic`).
* `--observation`: Stanovení tepelně-řízeného pozorování (`constant` nebo `sigmoid`). 

V případě nastavení logaritmického nebo rekurzivně-logaritmického chladicího plánu nebude uvažováno nastavení míry ochlazování, neboť tyto plány ji nevyužívají.

Příklad použití při výchozím nastavení nezávislých parametrů:
```bash
python3 src/qiea.py qisa datasets/100.txt --cooling_rate 0.95 --cooling linear --observation constant
```
pro chladicí plán využívající míru ochlazování, jinak například:
```bash
python3 src/qiea.py qisa datasets/100.txt --cooling logarithmic --observation sigmoid
```

### *QSE*
Kvantová evoluce roje má pouze jeden přídavný parametr a to:
* `--velocity`: Počáteční rychlost jednotlivých částic.

Příklad použití při výchozím nastavení nezávislých parametrů:
```bash
python3 src/qiea.py qse datasets/100.txt --velocity 5
```

### *QIPSO*
Kvantově inspirovaná optimalizace rojem částic má k dispozici následující přídavné parametry:
* `--c1`: Určení hodnoty kognitivního koeficientu.
* `--c2`: Určení hodnoty sociálního koeficientu.
* `--omega`: Určení koeficientu zúžení.
* `--velocity`: Počáteční rychlost jednotlivých částic.

Příklad použití při výchozím nastavení nezávislých parametrů:
```bash
python3 src/qiea.py qipso datasets/100.txt --c1 0.33 --c2 0.66 --omega 0.05 --velocity 50
```

## Spouštění experimentů
Všechny experimenty na všech velikostech instancí je možné spustit jako
```bash
make exp-all
```
případně je možné specifikovat pro jaký algoritmus mají být spuštěny experimenty na všech instancích a to jako:
```bash
make exp-[alg]
```
kde `alg` je zvolený *QIEA*, který může být jeden z následujících: `qiga`, `qisa`, `qipso` nebo `qse`.

Dále je možné specifikovat i velikost instance s jakou mají být provedeny experimenty daného *QIEA* a to následovně:
```bash
make exp-[alg]-[inst]
```
kde `inst` je velikost instance, která může být jedna z následujících: `100`, `250`, `500`, `1000`, `2000`, `5000` nebo `10000`. 

Všechny výše zmíněné experimenty budou provedeny pomocí 30 nezávislých běhů na konkrétní nastavení vybraného *QIEA* při 10000 evaluacích fitness funkce. 

Pro spuštění experimentů při počtu evaluací 100000 je možné použít následující příkaz:
```bash
make exp-large-[inst]
```
kde `inst` je velikost instance. Pomocí tohoto příkazu bude pro každý z algoritmů spuštěno 30 nezávislých běhů pro vybrané nastavení. Každý běh bude spuštěn za pomoci příkazu `nohup`(pro běh i po odhlášení či zavření terminálu) a `nice` (pro nižší prioritu procesu). 
Případně je možné nahradit `inst` slovem `all` pro spuštění všech algoritmů na všech velikostech instancí. 
Zachycené výpisy na příkazovou řádku budou uloženy do složky `logs/`.

V případě využití příkazu `make` je implicitně zvolena pro uložení výsledků experimentů složka `outputs/`.

## Generování grafů
Grafy všech algoritmů a všech instancí je možno vykreslit pomocí následujícího příkazu:
```bash
make graphs
```
kdy se předpokládá, že data experimentů se budou nacházet ve složce `outputs/`. Vygenerované grafy společně s vybranými statistikami dat, jež jsou zapsány do `.csv` souborů, jsou uloženy do složky `graphs/`.

Případně je možné parametrizovat samotné generování grafů jako
```bash
python3 src/plots.py outputs/ −−save_dir graphs/ −−algorithm {alg} −−instance {inst}
```
kde `alg`, respektive `inst`, jsou algoritmy, respektive instance, jejichž grafy mají být vykresleny. V případě specifikace konkrétního algoritmu nedojde k vykreslení porovnávacího grafu všech algoritmů. 

Příklady spuštění jsou
```bash
python3 src/plots.py outputs/ −−save_dir graphs/ −−algorithm qiga −−instance 5000
```
pro vykreslení grafů algoritmu *QIGA* a instance velikosti 500 nebo například:
```bash
python3 src/plots.py outputs/ −−save_dir graphs/ −−algorithm qse qipso −−instance 1000 2000
```
pro vykreslení grafů algoritmů *QSE* a *QIPSO* pro velikost instancí 1000 a 2000.
```bash
python3 src/plots.py outputs/ −−save_dir graphs/ −−algorithm qse qipso −−instance 1000 2000
```

V případě nezadání výstupního adresáře budou grafy zobrazeny v okně. 
Více informací o parametrizaci vykreslování grafů vizte:
```bash
python3 src/plots.py −−help
```

## Poznámka
Implementace algoritmu *QIGA* vychází z následujících implementací:
* [mjBM/Quantum-Evolutionary-Algorithm-Knapsack-Python-](https://github.com/mjBM/Quantum-Evolutionary-Algorithm-Knapsack-Python-),
* [Mousatat/Natural-Inspired-Computing-Project](https://github.com/Mousatat/Natural-Inspired-Computing-Project),

přičemž obě vycházejí z článku [Quantum-inspired evolutionary algorithm for a class of combinatorial optimization
](https://doi.org/10.1109/TEVC.2002.804320). Implementace byly navíc rozšířeny a optimalizovány pomocí knihovny `numpy`.