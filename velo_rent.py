# download modsim.py if necessary

from os.path import basename, exists

import matplotlib.pyplot as plt

from modsim import State, TimeSeries, flip


# import functions from modsim
def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print(f"Downloaded {local}")


download("https://github.com/AllenDowney/ModSimPy/raw/master/modsim.py")


bikeshare = State(mailly=10, moulin=2)


def velo_a_mailly():
    # print('Moving a bike to moulin')
    bikeshare.mailly -= 1
    bikeshare.moulin += 1


def velo_a_moulin():
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
        results[i] = bikeshare.mailly
    return results


res = run_simulation(10000, 0.5, 0.4)

fig, ax = plt.subplots()
ax.plot(res)
ax.set_title("Velos à Mailly")
ax.set_xlabel("Temps")
ax.set_ylabel("nombre")
plt.savefig("mailly.png")

def calculer_mecontentement(nb_velos, nb_velos_optimal=5):
    mecontentement = abs(nb_velos - nb_velos_optimal)
    return mecontentement

def run_simulation_with_mecontentement(num_steps, p1, p2):
    results = TimeSeries()
    mecontentement_series = TimeSeries()
    
    nb_velos_optimal = 5

    results[0] = bikeshare.mailly
    mecontentement_series[0] = calculer_mecontentement(bikeshare.mailly, nb_velos_optimal)
    
    for i in range(1, num_steps + 1):
        step(p1, p2)
        results[i] = bikeshare.mailly
        mecontentement_series[i] = calculer_mecontentement(bikeshare.mailly, nb_velos_optimal)
    
    return results, mecontentement_series

results, mecontentement = run_simulation_with_mecontentement(10000, 0.5, 0.4)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

ax1.plot(results)
ax1.set_title("Nombre de vélos à Mailly")
ax1.set_xlabel("Temps")
ax1.set_ylabel("Nombre de vélos")

ax2.plot(mecontentement, color='red')
ax2.set_title("Mécontentement à Mailly")
ax2.set_xlabel("Temps")
ax2.set_ylabel("Mécontentement")

plt.tight_layout()
plt.savefig("mailly_mecontentement.png")