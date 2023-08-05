# GrapeInSilico

## Introduction
GrapeInSilico is a user oriented and specialised modelling and simulation environment for the vine and the vineyard. It includes contributions from a large circle of researchers (4 laboratories are involved: LEPSE, AGAP, EFGV & SAVE). The main stake is the advancement of a collective modelling strategy that facilitates the transmission, the sharing and the valorisation of knowledge that is currently dispersed in different models that are not directly interoperable. Main applications are dedicated to the simulation of carbon balance and water fluxes within the plant and towards the fruits from different types of input data (manual measurements, digitizing, T-LiDAR). The platform also includes models allowing the estimation of the impact of fungal disease on growing structures depending on the developmental stages of the plant.

## Installation

At first you make sure that you have installed the package manager conda in your system: follow the instructions at https://docs.conda.io/en/latest/miniconda.html

Then we create a conda environment:

      conda create -n GIS -c openalea3 -c conda-forge openalea.plantgl pyqglviewer python=3.8
      conda activate GIS
      conda install -c openalea3 -c conda-forge numpy scipy qtconsole pandas matplotlib openalea.sconsx networkx ipykernel ipyparallel pytest rpy2 path

Clone the following repositories from github.com/openalea:

*    deploy
*    core
*    grapheditor
*    oalab
*    openalea-components
*    visualea
*    hydroshoot

Checkout the visualea branch in all the above except from deploy & hydroshoot (main).

Install each module using the develop mode
```python setup.py develop```     (in openalea-components it is ```multisetup.py```)

Clone from openalea-incubator:
    
*    TopVine
*    VirtualBerry
*    m2a3pc

Install each module using the develop mode
```python setup.py develop```    _(m2a3pc fails in windows cause of some lost path)_
