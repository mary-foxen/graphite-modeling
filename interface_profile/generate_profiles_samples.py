import pandas as pd
import numpy as np
from ast import literal_eval

df = pd.read_csv("fusion add-in/graphite_points.csv")
df['xs'] = [literal_eval(res) for res in df['xs']]
df['ys_bottom'] = [np.array(literal_eval(res)) for res in df['ys_bottom']]
df['ys_top'] = [np.array(literal_eval(res)) for res in df['ys_top']]
scale = 3.11/3
df['ys_top'] = [(res-0.15)*scale+0.15 for res in df['ys_top']]
df['ys_bottom'] = [(res-0.15)*scale+0.15 for res in df['ys_bottom']]
ys_top = []
for res in df['ys_top']:
    ys_top.append(list(res))
df['ys_top'] = ys_top
ys_bottom = []
for res in df['ys_bottom']:
    ys_bottom.append(list(res))
df['ys_bottom'] = ys_bottom
df.to_csv('fusion add-in/graphite_points_S3.csv', index=False)
