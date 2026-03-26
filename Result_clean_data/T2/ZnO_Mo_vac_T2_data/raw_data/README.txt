# README
This folder contains the raw data and the plotting script for the coherence analysis of Nb vacancies and Mo vacancies.

## Data format
In all raw data files:
- the first column is time (ms),
- the second column is the coherence function.

## Folder structure

### coh_plot.ipynb
Plotting script used to generate the figures in the main article and the Supplementary Information (written in Jupyter notebook).

### 'nb_v/'
Raw coherence data for Nb vacancies, including T2 and T2*.

### 'mo_v/'
Raw coherence data for Mo vacancies, including T2 and T2*. 'no_Q/' folder includes data for the SI Figure 11b 

### 'elec_bath/'
Raw coherence data for different electronic spin bath concentrations (0.1, 1, 10, and 100 ppm).  
These data were used to generate Figure 6 of the main article.

### 'conv_test/'
Raw data for convergence tests in Supplementary Information with respect to the size of the nuclear spin bath and the electronic spin bath.
