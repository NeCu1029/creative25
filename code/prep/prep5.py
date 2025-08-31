import warnings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Stations, Hourly

warnings.filterwarnings("ignore")

matches = pd.read_csv("preps/match2.csv")
for x in range(166, len(matches)):
    se = matches.iloc[x]
    prv_info = pd.read_csv(f"preps/info/info{int(se["date"])}.csv")
    prv_data = pd.read_csv(f"preps/data/data{int(se["date"])}.csv")
    nxt_data = pd.read_csv(f"preps/data/data{int(se["date"]) + 1}.csv")
    prv_cluster = int(se["prv_cluster"])

    fire = prv_data[prv_data["cluster"] == prv_cluster]
    fire2 = pd.DataFrame(columns=["lon", "lat", "pixels", "vx", "vy", "hum"])
    cnt = 0
    start = datetime(2022, 4, 1, 0, 0, 0) + timedelta(days=int(se["date"]))
    milon = prv_info[prv_info["cluster"] == prv_cluster].iloc[0]["min_lon"]
    malon = prv_info[prv_info["cluster"] == prv_cluster].iloc[0]["max_lon"]
    milat = prv_info[prv_info["cluster"] == prv_cluster].iloc[0]["min_lat"]
    malat = prv_info[prv_info["cluster"] == prv_cluster].iloc[0]["max_lat"]
    milon = (milon * 2 // 1) / 2
    malon = (malon * 2 // 1) / 2
    milat = (milat * 2 // 1) / 2
    malat = (malat * 2 // 1) / 2
    print(milon, malon, milat, malat)
    for lon in np.arange(milon, malon + 0.1, 0.5):
        for lat in np.arange(milat, malat + 0.1, 0.5):
            sts = Stations().bounds((lat + 0.5, lon), (lat, lon + 0.5))
            l = sts.count()
            sts = sts.fetch()
            if l == 0:
                fire2.loc[cnt] = pd.Series(
                    [lon, lat, 0, np.nan, np.nan, np.nan],
                    index=["lon", "lat", "pixels", "vx", "vy", "hum"],
                )
                cnt += 1
                continue
            vx, vy, hum = 0.0, 0.0, 0.0
            for station in sts.index:
                data = Hourly(station, start, start + timedelta(0, 86399)).fetch()
                vx += (np.cos(data["wdir"] * np.pi / 180) * data["wspd"]).mean()
                vy += (np.sin(data["wdir"] * np.pi / 180) * data["wspd"]).mean()
                hum += data["rhum"].mean()
            fire2.loc[cnt] = pd.Series(
                [lon, lat, 0, vx / l, vy / l, hum / l],
                index=["lon", "lat", "pixels", "vx", "vy", "hum"],
            )
            cnt += 1
            print(lon, lat)
    for i in range(len(fire)):
        lon = (fire.iloc[i]["lon"] * 2 // 1) / 2
        lat = (fire.iloc[i]["lat"] * 2 // 1) / 2
        print(lon, lat, "*")
        idx = fire2[fire2["lon"] == lon][fire2["lat"] == lat].index[0]
        fire2.loc[idx, "pixels"] += 1  # type: ignore
    fire2.to_csv(
        f"C:/Users/ljw10/Desktop/LeeJunWoo/gshs/contest/creative25/data/{x}.csv",
        index=False,
    )

    label = nxt_data[nxt_data["cluster"] == int(se["cluster"])]
    label2 = pd.DataFrame(columns=["lon", "lat", "pixels"])
    chk = set()
    cnt = 0
    for i in range(len(label)):
        lon = (label.iloc[i]["lon"] * 2 // 1) / 2
        lat = (label.iloc[i]["lat"] * 2 // 1) / 2
        if (lon, lat) in chk:
            idx = label2[label2["lon"] == lon][label2["lat"] == lat].index[0]
            label2.loc[idx, "pixels"] += 1  # type: ignore
        else:
            chk.add((lon, lat))
            label2.loc[cnt] = pd.Series([lon, lat, 1], index=["lon", "lat", "pixels"])
            cnt += 1
    label2.to_csv(
        f"C:/Users/ljw10/Desktop/LeeJunWoo/gshs/contest/creative25/label/{x}.csv",
        index=False,
    )
    print(x)
    print()
