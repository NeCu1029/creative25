import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings(action="ignore")


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    )
    return 6371 * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def haversine_vectorized(coords1, coords2):
    lat1 = coords1[:, 0][:, np.newaxis]
    lon1 = coords1[:, 1][:, np.newaxis]
    lat2 = coords2[:, 0][np.newaxis, :]
    lon2 = coords2[:, 1][np.newaxis, :]
    return haversine_distance(lat1, lon1, lat2, lon2)


def find_nearest_points(df_a: pd.DataFrame, df_b: pd.DataFrame, i):
    coords_a = df_a[["cm_lat", "cm_lon"]].values
    coords_b = df_b[["cm_lat", "cm_lon"]].values

    distances = haversine_vectorized(coords_b, coords_a)
    nearest_indices = np.argmin(distances, axis=1)
    min_distances = distances[np.arange(len(df_b)), nearest_indices]

    result = df_b.iloc[:, [0, 2, 5]]
    result["date"] = i
    result["prv_cluster"] = df_a.iloc[nearest_indices]["cluster"].values
    result["dist"] = min_distances
    return result[
        [
            "date",
            "cluster",
            "prv_cluster",
            "dist",
        ]
    ]


dfs = []
for i in range(29):
    df_a = pd.read_csv(f"preps/info/info{i}.csv")
    df_b = pd.read_csv(f"preps/info/info{i + 1}.csv")

    res = find_nearest_points(df_a, df_b, i)
    dfs.append(res)
result = pd.concat(dfs)
result.to_csv(
    "C:/Users/ljw10/Desktop/LeeJunWoo/gshs/contest/creative25/preps/match.csv",
    index=False,
)
