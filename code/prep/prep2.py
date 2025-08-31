import pandas as pd

for fi in range(30):
    full = pd.read_csv(f"preps/data/data{fi}.csv")
    dfs = [dat for _, dat in full.groupby("cluster")]

    res = pd.DataFrame(
        columns=[
            "cluster",
            "min_lon",
            "cm_lon",
            "max_lon",
            "min_lat",
            "cm_lat",
            "max_lat",
        ]
    )
    idx = 0
    for df in dfs:
        cur = pd.Series()
        cur["cluster"] = df["cluster"].iloc[0]
        cur["min_lon"] = df["lon"].min()
        cur["cm_lon"] = round((df["lon"] * df["pixels"]).sum() / df["pixels"].sum(), 3)
        cur["max_lon"] = df["lon"].max()
        cur["min_lat"] = df["lat"].min()
        cur["cm_lat"] = round((df["lat"] * df["pixels"]).sum() / df["pixels"].sum(), 3)
        cur["max_lat"] = df["lat"].max()
        res.loc[idx] = cur
        idx += 1

    res = res.astype({"cluster": "int32"})
    res.to_csv(
        f"C:/Users/ljw10/Desktop/LeeJunWoo/gshs/contest/creative25/preps/info/info{fi}.csv",
        index=False,
    )
