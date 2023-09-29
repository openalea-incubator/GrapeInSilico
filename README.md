# GrapeInSilico

## Introduction
GrapeInSilico is a user oriented and specialised modelling and simulation environment for the vine and the vineyard. It includes contributions from a large circle of researchers (4 laboratories are involved: LEPSE, AGAP, EFGV & SAVE). The main stake is the advancement of a collective modelling strategy that facilitates the transmission, the sharing and the valorisation of knowledge that is currently dispersed in different models that are not directly interoperable. Main applications are dedicated to the simulation of carbon balance and water fluxes within the plant and towards the fruits from different types of input data (manual measurements, digitizing, T-LiDAR). The platform also includes models allowing the estimation of the impact of fungal disease on growing structures depending on the developmental stages of the plant.

## Installation

At first you make sure that you have installed the package manager mamba in your system: follow the instructions at [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge).

Then we create a mamba environment:

      mamba create -n GIS -c openalea3 -c conda-forge openalea.visualea openalea.hydroshoot rpy2 openalea.sconsx
      mamba activate GIS

Clone from openalea-incubator:
    
*    TopVine
*    VirtualBerry
*    m2a3pc
*    GrapeInSilico

Install each module using the develop mode
```python setup.py develop```    _(m2a3pc fails in windows cause of some lost path)_
