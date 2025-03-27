# corr_pooling_replication_package

## Overview

This is the code package for the paper 'Correlation Improves Group Testing: Modeling Concentration-Dependent Test Errors', to appear in Management Science. We conduct rigorous theoretical analysis and realistic simulation to understand the benefit of accounting for correlation and concentration-dependent test errors in group testing for large-scale screening of infectious diseases.

We provide information about the simulation in this folder.

## Structure of the folder

- src
  - code for the simulation in section 4
  - script for running the simulation and generating raw data
- notebooks
  - converting raw data to aggregated data 
  - making plots
- data
  - raw
  - aggregated


## How to run simulation trials

Install conda environment using env_specs.txt, and activate the environment

Go to /src and run `bash _run_experiments.sh`

