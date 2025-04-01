# Replication package for 'Correlation Improves Group Testing: Modeling Concentration-Dependent Test Errors'


## Overview


This is the code package for the paper 'Correlation Improves Group Testing: Modeling Concentration-Dependent Test Errors', to appear in Management Science. We conduct rigorous theoretical analysis and realistic simulation to understand the benefit of accounting for correlation and concentration-dependent test errors in group testing for repeated large-scale screening of infectious diseases.


We provide information about the simulation in this folder.


## Structure of the folder


- src/
	- Our simulation codebase is partly based on the SEIRS+ library (https://github.com/ryansmcgee/seirsplus). In particular, `FARZ.py`, `models.py`, `networks.py`, and `utilities.py` are inherited from SEIRS+. 
	- `assignment.py`: assignment of screening groups and formation of community and household-correlated pools.
	- `pooled_test.py`: implementation of the two-stage Dorfman procedure.
	- `viral_model.py`: an extended SEIRS+ stochastic network model, `ViralExtSEIRNetworkModel`, where each node has a viral load that is dynamically updated as time progresses and they transition through different states. 
	- `sim_loops_pooled_test.py`: the runner class of the `ViralExtSEIRNetworkModel` model 	that enables simulation and logging.
	- `run_meta_simulation_g2.py`: the wrapper functions for running simulation of different configurations.
	- `run_experiments.sh`: the master script for running multiple replications of simulations of different configurations.

- data/
	- raw/
	- aggregated/
	- aggregated_final/

- notebooks/
	- converting raw simulation results to aggregated data
	- making figures

- figures/


Our results in the paper are based on 200 trials per parameter configuration (screening policy and test error model). We aggregate the raw simulation results by computing several key metric statistics, which are then used for further analysis and visualization. 


Here, we demonstrate how to run 10 trials for an example policy of screening every 5 days using a pool size of 10, under a test error model that accounts for the dilution effect. The script `src/run_experiments.sh` initiates the simulation runs with results saved under `data/raw/`. On a 4-core machine with 32GB memory, one simulation run for naive pooling takes 10-20 minutes; one simulation run for correlated pooling takes 3-4 hours. The notebook `notebooks/aggregate_raw_data.ipynb` shows how to convert the raw simulation results into aggregated data files, saved under `data/aggregated/`.


We also include the aggregated data from the complete simulation runs under `data/aggregated_final/`. The notebook `notebooks/aggregate_raw_data_final.ipynb` logs the process of converting the complete raw simulation results into aggregated files. All figure reproduction notebooks are based on the data in `data/aggregated_final/`.


## How to run simulation trials


Create a conda environment. Activate the environment, and install the necessary packages using 
```sh
pip install -r requirements.txt
```
Then, run 
```sh
bash src/run_experiments.sh
```
for a 10-trial example.

