import pygrib
from datetime import datetime


def read_grib(file_path):
    dataset = pygrib.open(file_path)
    prcp_data = dataset.select(shortName='tp', level=0, typeOfLevel='surface')
    mslp_data = dataset.select(shortName='msl', level=0, typeOfLevel='surface')

    lats, lons = dataset.select(shortName='msl', level=0, typeOfLevel='surface')[0].latlons()

    arrs = list(map(grb_msg2arr, zip(prcp_data, mslp_data)))

    return arrs, lats, lons


def grb_msg2arr(grb_data):
    prcp, mslp = grb_data

    assert prcp.validityDate == mslp.validityDate
    assert prcp.validityTime == mslp.validityTime

    validity_date = str(mslp.validityDate)
    validity_time= str(mslp.validityTime).zfill(4)

    validity_dt = datetime.strptime(f'{validity_date} {validity_time}', '%Y%m%d %H%M')

    prcp_arr = prcp.values * 1000
    mslp_arr = mslp.values * 0.01

    return (prcp_arr, mslp_arr, validity_dt)
