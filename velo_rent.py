import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def State(**variables):
    """Contains the values of state variables."""
    return pd.Series(variables, name='state')

def flip(p=0.5):
    """Flips a coin with the given probability.

    p: float 0-1

    returns: boolean (True or False)
    """
    return np.random.random() < p


def TimeSeries(*args, **kwargs):
    """Make a pd.Series object to represent a time series.
    """
    if args or kwargs:
        #underride(kwargs, dtype=float)
        series = pd.Series(*args, **kwargs)
    else:
        series = pd.Series([], dtype=float)

    series.index.name = 'Time'
    if 'name' not in kwargs:
        series.name = 'Quantity'
    return series

bikeshare = State(mailly=10, moulin=2)


def velo_a_moulin():
    # print('Moving a bike to moulin')
    bikeshare.mailly -= 1
    bikeshare.moulin += 1


def velo_a_mailly():
    # print('Moving a bike to mailly')
    bikeshare.moulin -= 1
    bikeshare.mailly += 1


def step(p1, p2):
    if flip(p1):
        velo_a_mailly()

    if flip(p2):
        velo_a_moulin()




def run_simulation(numstep, p1, p2):
    results = TimeSeries()
    results[0] = bikeshare.mailly
    for i in range(numstep):
        step(p1, p2)
        results[i + 1] = bikeshare.mailly
    return results

numstep, p1, p2 = 100, 0.5, 0.47
res = run_simulation(numstep, p1, p2)

fig, ax = plt.subplots()
ax.plot(res)
ax.set_title("Velos à Mailly")
ax.set_xlabel("Temps")
ax.set_ylabel("nombre")
plt.savefig("mailly.png")
