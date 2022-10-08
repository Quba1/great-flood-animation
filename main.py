from functools import partial
import matplotlib.pyplot as plt
import gc
from multiprocessing import Pool

from pymodules.read_grib import read_grib
from pymodules.plot_map import plot_map


def main():
    gc.enable()
    plt.rcParams["font.family"] = "Fira Mono"

    arrs, lats, lons = read_grib(f'./data/era5-mslp-precip.grib')

    plot_fn = partial(plot_map, lats=lats, lons=lons)

    with Pool(8) as p:
        p.map(plot_fn, arrs)


if __name__ == "__main__":
    main()
