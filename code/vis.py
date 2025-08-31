import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

with open("filename.txt") as f:
    s = f.readlines()
    ds = xr.open_dataset(f"copernicus/{s[1].rstrip()}")
    fire_data = ds["fire_pixels"].isel(time=0)
    fire_values = fire_data.values
    lon_values = fire_data.lon.values
    lat_values = fire_data.lat.values

    fire_coords = []
    fire_pixel_values = []
    non_zero_indices = np.where(fire_values != 0)

    for i, j in zip(non_zero_indices[0], non_zero_indices[1]):
        lat = lat_values[i]
        lon = lon_values[j]
        fire_coords.append((lon, lat))
        fire_pixel_values.append(fire_values[i, j])

    coor = np.array([tuple(map(lambda x: round(x, 2), i)) for i in fire_coords])
    fire_pixel_values = np.array(fire_pixel_values)
    dbscan = DBSCAN(eps=2, min_samples=3)
    dbscan.fit(coor)

    m1 = dbscan.labels_ == -1
    f1 = coor[m1]
    m2 = dbscan.labels_ != -1
    f2 = coor[m2]
    plt.scatter(f1[:, 0], f1[:, 1], s=0.1, c="red")
    plt.scatter(f2[:, 0], f2[:, 1], s=0.1, c="blue")
    plt.xlim(-180, 180)
    plt.xlabel("longitude")
    plt.ylim(-90, 90)
    plt.ylabel("latitude")
    plt.title("DBSCAN clustering (red = outliers)")
    plt.show()
