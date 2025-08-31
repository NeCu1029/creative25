import xarray as xr
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

with open("filename.txt") as f:
    s = f.readlines()

for fi in range(1, 60, 2):
    ds = xr.open_dataset(f"copernicus/{s[fi].rstrip()}")
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
    fire_coords = np.array(fire_coords)
    fire_pixel_values = np.array(fire_pixel_values)
    dbscan = DBSCAN(eps=2, min_samples=3)
    dbscan.fit(coor)

    dfs = []
    for label in np.unique(dbscan.labels_):
        mask = dbscan.labels_ == label
        if label != -1 and mask.sum() >= 5 and fire_pixel_values[mask].sum() >= 15:
            mask_coord = fire_coords[mask]
            mask_pixel = fire_pixel_values[mask]
            for i in range(len(mask_coord)):
                new = pd.DataFrame(
                    {
                        "cluster": [label],
                        "idx": [i],
                        "lon": [round(mask_coord[i][0], 2)],
                        "lat": [round(mask_coord[i][1], 2)],
                        "pixels": [mask_pixel[i]],
                    }
                )
                dfs.append(new)
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(
        f"C:/Users/ljw10/Desktop/LeeJunWoo/gshs/contest/creative25/preps/data/data{fi // 2}.csv",
        index=False,
    )
    print(fi)
