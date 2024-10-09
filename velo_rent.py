#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Pool

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


bikeshare = State(mailly=10, moulin=10, discontent=0)


def move_bike(from_station, to_station):
    """Move a bike from one station to another station if possible."""
    if getattr(bikeshare, from_station) > 0:
        setattr(bikeshare, from_station, getattr(bikeshare, from_station) - 1)
        setattr(bikeshare, to_station, getattr(bikeshare, to_station) + 1)
    else:
        bikeshare.discontent += 1



def step(p1, p2, user_state, bikeshare):
    if user_state.users_moulin > 0 and flip(p1):
        move_bike("moulin", "mailly",)

    if user_state.users_mailly > 0 and flip(p2):
        move_bike("mailly", "moulin")


def run_simulation(num_steps, p1, p2, starting_users_mailly, starting_users_moulin, velos_moulin=20, velos_mailly=20):
    bikeshare = State(mailly=velos_mailly, moulin=velos_moulin, discontent=0)
    user_state = State(users_mailly=starting_users_mailly, users_moulin=starting_users_moulin)
    results = TimeSeries()
    discontent = TimeSeries()
    results[0] = bikeshare.mailly
    discontent[0] = bikeshare.discontent
    counter = 0
    for i in range(num_steps):
        if counter % (24*7) == 0:
            bikeshare.mailly = velos_mailly
            bikeshare.moulin = velos_moulin
        counter += 1
        if user_state.users_moulin > 0 and flip(p1):
            if bikeshare.moulin > 0:
                bikeshare.moulin -= 1
                bikeshare.mailly += 1
            else:
                bikeshare.discontent += 1
            
        if user_state.users_mailly > 0 and flip(p2):
            if bikeshare.mailly > 0:
                bikeshare.moulin += 1
                bikeshare.mailly -= 1
            else:
                bikeshare.discontent += 1
        results[i + 1] = bikeshare.mailly
        discontent[i + 1] = bikeshare.discontent
    return [results, discontent]


def run_simulations_in_parallel(params_list):
    with Pool(3) as p:
        result = p.starmap_async(run_simulation, params_list)
        return result.get()


params_list = [
    (10000, 0.5, 0.47, 10, 10, 20, 20),
    (10000, 0.5, 0.33, 20, 25, 20, 20),
    (10000, 0.47, 0.6, 15, 15, 20, 20),
]
res1, res2, res3 = run_simulations_in_parallel(params_list)

#res1 = run_simulation(10000, 0.5, 0.47, 10, 10, 20, 20)
#res2 = run_simulation(10000, 0.5, 0.33, 20,  5, 20, 20)
#res3 = run_simulation(10000, 0.47, 0.6, 15, 15, 20, 20)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
ax1.plot(res1[0], color="blue")
ax1.plot(res1[1], color="red")
ax1.set_title("Velos à Mailly")
ax1.set_xlabel("0.5, 0.47, 10, 10")
ax1.set_ylabel("nombre")

ax2.plot(res2[0], color="blue")
ax2.plot(res2[1], color="red")
ax2.set_xlabel("0.5, 0.33, 20, 25")
ax2.set_ylabel("nombre")

ax3.plot(res3[0], color="blue")
ax3.plot(res3[1], color="red")
ax3.set_xlabel("0.47, 0.6, 15, 15")
ax3.set_ylabel("nombre")

plt.savefig("mailly.png")
