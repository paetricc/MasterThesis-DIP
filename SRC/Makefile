#####################################
# Autor: Tomáš Bártů                #
# Email: xbartu11@stud.fit.vutbr.cz #
#####################################
SHELL=/bin/bash

# Definitions
PYTHON=python3
GRAPHS_SOURCE_DIR=outputs
GRAPHS_OUTPUT_DIR=graphs

.PHONY: graphs

#######################
##### EXPERIMENTS #####
#######################
# all experiments
exp-all: exp-qiga exp-qisa exp-qse exp-qipso


####################################
# Quantum Inspired Genetic Algorithm
####################################
# all experiments for qiga
exp-qiga: exp-qiga-100 exp-qiga-250 exp-qiga-500 exp-qiga-1000 exp-qiga-2000 exp-qiga-5000 exp-qiga-10000
# experiment for knapsack instance size 100
exp-qiga-100:
	./scripts/qiga/qiga_experiments_100.sh
# experiment for knapsack instance size 250
exp-qiga-250:
	./scripts/qiga/qiga_experiments_250.sh
# experiment for knapsack instance size 500
exp-qiga-500:
	./scripts/qiga/qiga_experiments_500.sh
# experiment for knapsack instance size 1000
exp-qiga-1000:
	./scripts/qiga/qiga_experiments_1000.sh
# experiment for knapsack instance size 2000
exp-qiga-2000:
	./scripts/qiga/qiga_experiments_2000.sh
# experiment for knapsack instance size 5000
exp-qiga-5000:
	./scripts/qiga/qiga_experiments_5000.sh
# experiment for knapsack instance size 10000
exp-qiga-10000:
	./scripts/qiga/qiga_experiments_10000.sh
####################################


######################################
# Quantum Inspired Simulated Annealing
######################################
# all experiments for qse
exp-qisa: exp-qisa-100 exp-qisa-250 exp-qisa-500 exp-qisa-1000 exp-qisa-2000 exp-qisa-5000 exp-qisa-10000
# experiment for knapsack instance size 100
exp-qisa-100:
	./scripts/qisa/qisa_experiments_100.sh
# experiment for knapsack instance size 250
exp-qisa-250:
	./scripts/qisa/qisa_experiments_250.sh
# experiment for knapsack instance size 500
exp-qisa-500:
	./scripts/qisa/qisa_experiments_500.sh
# experiment for knapsack instance size 1000
exp-qisa-1000:
	./scripts/qisa/qisa_experiments_1000.sh
# experiment for knapsack instance size 2000
exp-qisa-2000:
	./scripts/qisa/qisa_experiments_2000.sh
# experiment for knapsack instance size 5000
exp-qisa-5000:
	./scripts/qisa/qisa_experiments_5000.sh
# experiment for knapsack instance size 10000
exp-qisa-10000:
	./scripts/qisa/qisa_experiments_10000.sh
######################################


############################
# Quantum Swarm Evolutionary
############################
# all experiments for qse
exp-qse: exp-qse-100 exp-qse-250 exp-qse-500 exp-qse-1000 exp-qse-2000 exp-qse-5000 exp-qse-10000
# experiment for knapsack instance size 100
exp-qse-100:
	./scripts/qse/qse_experiments_100.sh
# experiment for knapsack instance size 250
exp-qse-250:
	./scripts/qse/qse_experiments_250.sh
# experiment for knapsack instance size 5000
exp-qse-500:
	./scripts/qse/qse_experiments_500.sh
# experiment for knapsack instance size 1000
exp-qse-1000:
	./scripts/qse/qse_experiments_1000.sh
# experiment for knapsack instance size 2000
exp-qse-2000:
	./scripts/qse/qse_experiments_2000.sh
# experiment for knapsack instance size 5000
exp-qse-5000:
	./scripts/qse/qse_experiments_5000.sh
# experiment for knapsack instance size 10000
exp-qse-10000:
	./scripts/qse/qse_experiments_10000.sh
############################


##############################################
# Quantum Inspired Particle Swarm Optimization
##############################################
# all experiments for qipso
exp-qipso: exp-qipso-100 exp-qipso-250 exp-qipso-500 exp-qipso-1000 exp-qipso-2000 exp-qipso-5000 exp-qipso-10000
# experiment for knapsack instance size 100
exp-qipso-100:
	./scripts/qipso/qipso_experiments_100.sh
# experiment for knapsack instance size 250
exp-qipso-250:
	./scripts/qipso/qipso_experiments_250.sh
# experiment for knapsack instance size 500
exp-qipso-500:
	./scripts/qipso/qipso_experiments_500.sh
# experiment for knapsack instance size 1000
exp-qipso-1000:
	./scripts/qipso/qipso_experiments_1000.sh
# experiment for knapsack instance size 2000
exp-qipso-2000:
	./scripts/qipso/qipso_experiments_2000.sh
# experiment for knapsack instance size 5000
exp-qipso-5000:
	./scripts/qipso/qipso_experiments_5000.sh
# experiment for knapsack instance size 10000
exp-qipso-10000:
	./scripts/qipso/qipso_experiments_10000.sh
##############################################


##########################################
# Quantum Inspired Evolutionary Algorithms
# *large instances of knapsack 0-1* 
##########################################
# all experiments for large instances
exp-large-all: exp-large-1000 exp-large-2000 exp-large-5000 exp-large-10000
# experiments for knapsack instance size 1000
exp-large-1000:
	./scripts/large/large_experiments_1000.sh
# experiments for knapsack instance size 2000
exp-large-2000:
	./scripts/large/large_experiments_2000.sh
# experiments for knapsack instance size 5000
exp-large-5000:
	./scripts/large/large_experiments_5000.sh
# experiments for knapsack instance size 10000
exp-large-10000:
	./scripts/large/large_experiments_10000.sh
##########################################

#######################
### END EXPERIMENTS ###
#######################

###########################
##### GRAPHS PLOTTING #####
###########################
graphs:
	@if [ -d "$(GRAPHS_SOURCE_DIR)" ]; then \
		echo "Generating graphs..."; \
		if [ "$(ALGORITHM)" ]; then \
			$(PYTHON) src/plots.py --save_dir $(GRAPHS_OUTPUT_DIR) --algorithm $(ALGORITHM) $(GRAPHS_SOURCE_DIR); \
		else \
			$(PYTHON) src/plots.py --save_dir $(GRAPHS_OUTPUT_DIR) $(GRAPHS_SOURCE_DIR); \
		fi; \
	else \
		echo "Directory $(GRAPHS_SOURCE_DIR) does not exist."; \
	fi
### END GRAPHS PLOTTING ###