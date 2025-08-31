import pandas as pd

src = pd.read_csv("preps/match.csv")
dfs = [dat for _, dat in src.groupby("date")]
res = []

for i in range(29):
    prv = pd.read_csv(f"preps/info/info{i}.csv")
    nxt = pd.read_csv(f"preps/info/info{i + 1}.csv")
    sp = [dat for _, dat in dfs[i].groupby("prv_cluster")]

    for j in sp:
        if len(j) > 1 or j["dist"].iloc[0] >= 500:
            continue
        res.append(j)

result = pd.concat(res)
result.to_csv(
    "C:/Users/ljw10/Desktop/LeeJunWoo/gshs/contest/creative25/preps/match2.csv",
    index=False,
)
