from souk import DATADIR
from souk.data.zemax import load_psf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from pathlib import Path


def import_grasp(filename):
    return np.loadtxt(filename, delimiter=",", skiprows=6)

def main():
    
