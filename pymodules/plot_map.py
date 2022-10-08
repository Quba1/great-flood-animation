import matplotlib.pyplot as plt
import gc
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy
from cartopy.mpl.geoaxes import GeoAxes


def configure_plot(fig):
    ax = GeoAxes(
        fig,
        [0, 0, 1, 1],
        yticks=[],
        xticks=[],
        frame_on=False,
        aspect='auto',
        projection=ccrs.Mercator(),
    )

    fig.delaxes(fig.gca())
    fig.add_axes(ax)

    ax.set_extent([5.0, 25.0, 42.0, 55.5], crs=ccrs.PlateCarree())
    # ax.add_feature(cfeature.LAND)
    # ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE, linestyle="-", alpha=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.BORDERS, linestyle="-", alpha=0.5)

    return fig, ax


def plot_map(grb_arr, lats, lons):
    prcp_arr, mslp_arr, validity_dt = grb_arr

    fig = plt.figure(figsize=(12, 12), dpi=100)

    fig, ax = configure_plot(fig)

    ax.contourf(
        lons,
        lats,
        prcp_arr,
        levels=numpy.arange(0, 15, .25),
        cmap='Blues',
        transform=ccrs.PlateCarree(),
    )

    CS = ax.contour(
        lons,
        lats,
        mslp_arr,
        levels=numpy.arange(970.0, 1040.0, 5.0),
        colors="gray",
        transform=ccrs.PlateCarree(),
    )
    ax.clabel(CS)

    dt_str = validity_dt.strftime('%Y%m%d%H%M')

    fig.savefig(f"./output/map-{dt_str}.png",
                bbox_inches="tight",
                pad_inches=0)
    plt.close(fig)
    gc.collect()
