import concurrent.futures

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def State(**variables):
    """Contains the values of state variables."""
    return pd.Series(variables, name="state")


def flip(p=0.5):
    """Flips a coin with the given probability.

    p: float 0-1

    returns: boolean (True or False)
    """
    return np.random.random() < p


def TimeSeries(*args, **kwargs):
    """Make a pd.Series object to represent a time series."""
    if args or kwargs:
        # underride(kwargs, dtype=float)
        series = pd.Series(*args, **kwargs)
    else:
        series = pd.Series([], dtype=float)

    series.index.name = "Time"
    if "name" not in kwargs:
        series.name = "Quantity"
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


def run_simulation(num_steps, p1, p2):
    results = TimeSeries()
    results[0] = bikeshare.mailly
    for i in range(num_steps):
        step(p1, p2)
        results[i + 1] = bikeshare.mailly
    return results


def run_simulations_in_parallel(params_list):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_simulation, *params) for params in params_list]
        return [future.result() for future in futures]


params_list = [(10000, 0.5, 0.47), (10000, 0.5, 0.33), (10000, 0.6, 0.47)]
res1, res2, res3 = run_simulations_in_parallel(params_list)


fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
ax1.plot(res1)
ax1.set_title("Velos à Mailly")
ax1.set_xlabel("Temps")
ax1.set_ylabel("nombre")

ax2.plot(res2)
ax2.set_title("Velos à Mailly")
ax2.set_xlabel("Temps")
ax2.set_ylabel("nombre")

ax3.plot(res3)
ax3.set_title("Velos à Mailly")
ax3.set_xlabel("Temps")
ax3.set_ylabel("nombre")

plt.savefig("mailly.png")
