import matplotlib.pyplot as plt
import gc

from pymodules.read_grib import read_grib
from pymodules.plot_map import plot_map


def main():
    gc.enable()
    plt.rcParams["font.family"] = "Fira Mono"

    arrs, lats, lons = read_grib(f'./data/era5-mslp-precip.grib')

    grb_arr = arrs[138]

    plot_map(grb_arr, lats, lons)


if __name__ == "__main__":
    main()
