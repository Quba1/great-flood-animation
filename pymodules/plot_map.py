from matplotlib import patches
import matplotlib
import matplotlib.pyplot as plt
import gc
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy
from cartopy.mpl.geoaxes import GeoAxes

from pymodules.colormaps import get_radar_cmap


def configure_plot(fig):
    ax = GeoAxes(
        fig,
        [0, 0, 1, 1],
        yticks=[],
        xticks=[],
        frame_on=True,
        aspect='auto',
        projection=ccrs.Mercator(),
    )

    fig.delaxes(fig.gca())
    fig.add_axes(ax)

    ax.set_extent([5.0, 25.0, 42.0, 55.5], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linestyle="-", alpha=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.BORDERS, linestyle="-", alpha=0.5)

    return fig, ax


def plot_map(grb_arr, lats, lons):
    prcp_arr, mslp_arr, validity_dt = grb_arr

    lons = lons[38:93, 40:121]
    lats = lats[38:93, 40:121]
    prcp_arr = prcp_arr[38:93, 40:121]
    mslp_arr = mslp_arr[38:93, 40:121]

    dbz_arr = prcp_arr
    dbz_arr[dbz_arr > 0] = 10 * numpy.log10(
        200 * (numpy.power(dbz_arr[dbz_arr > 0], 8 / 5)))

    fig = plt.figure(figsize=(12, 12), dpi=100)

    fig, ax = configure_plot(fig)

    im = ax.pcolormesh(
        lons,
        lats,
        dbz_arr,
        vmin=0.0,
        vmax=65.0,
        cmap=get_radar_cmap(0.7),
        transform=ccrs.PlateCarree(),
        zorder=3,
    )

    func = lambda x, pos: "{:.2f}".format(
        numpy.power((numpy.power(10, (x / 10.0)) / 200.0), 5 / 8))
    fmt = matplotlib.ticker.FuncFormatter(func)
    cax = fig.add_axes([1.03, 0.05, 0.02, 0.95])
    cbar = fig.colorbar(im, cax=cax, orientation='vertical', format=fmt)
    cbar.ax.tick_params(labelsize=14)

    CS = ax.contour(
        lons,
        lats,
        mslp_arr,
        levels=numpy.arange(970.0, 1040.0, 5.0),
        colors="gray",
        transform=ccrs.PlateCarree(),
        zorder=4,
    )
    ax.clabel(CS)

    dt_text = validity_dt.strftime("%Y-%m-%d %H:%M UTC")
    ax.add_patch(
        patches.Rectangle(xy=[20.0, 42.0],
                          width=5.0,
                          height=0.5,
                          facecolor='white',
                          transform=ccrs.PlateCarree(),
                          zorder=5))
    ax.text(0.775,
            0.01,
            f'{dt_text}',
            transform=ax.transAxes,
            fontsize=14,
            zorder=6)

    cax.text(0.0,
             -0.04,
             f'[mm/hr]',
             transform=cax.transAxes,
             fontsize=14,
             zorder=6)

    dt_str = validity_dt.strftime('%Y%m%d%H%M')

    fig.savefig(f"./output/map-{dt_str}.png",
                bbox_inches="tight",
                pad_inches=0.3)

    plt.close(fig)
    gc.collect()
