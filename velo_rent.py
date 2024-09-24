# download modsim.py if necessary

from os.path import basename, exists

import matplotlib.pyplot as plt


def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("Downloaded " + local)


download("https://github.com/AllenDowney/ModSimPy/raw/master/modsim.py")

# import functions from modsim

from modsim import State, TimeSeries, flip

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


results = TimeSeries()

results[0] = bikeshare.mailly

for i in range(60 * 14 * 30):
    # print(f"step {i}")
    step(0.5, 0.4)
    results[i + 1] = bikeshare.mailly

fig, ax = plt.subplots()
ax.plot(results)
ax.set_title("Velos à Mailly")
ax.set_xlabel("Temps")
ax.set_ylabel("nombre")
plt.show()

