import pandas as pd
import numpy as np
from ast import literal_eval
from scipy.interpolate import UnivariateSpline
from tqdm import tqdm
import os

df = pd.read_csv('fusion add-in/graphite_points.csv')
df['xs'] = [np.array(literal_eval(res)) for res in df['xs']]
df['ys_bottom'] = [np.array(literal_eval(res)) for res in df['ys_bottom']]
df['ys_top'] = [np.array(literal_eval(res)) for res in df['ys_top']]
values = []
graphite_thickness = 0.3
total_thickness = 0.315
graphite_width = 1
v_added_meas = graphite_thickness*graphite_width*0.2*1e-4
for scale in tqdm(np.linspace(0.01, 1, 100)):
    for porosity in np.linspace(0.01, 1, 100):
        for i in range(len(df)):
            df['ys_top_scaled'] = [(res-0.15)*scale+0.15 for res in df['ys_top']]
            df['ys_bottom_scaled'] = [(res-0.15)*scale+0.15 for res in df['ys_bottom']]
            xs = df['xs'][i]
            ys_top = df['ys_top'][i]
            ys_bottom = df['ys_bottom'][i]
            ys_top_scaled = df['ys_top_scaled'][i]
            ys_bottom_scaled = df['ys_bottom_scaled'][i]
            v_putty_flat = (total_thickness - graphite_thickness)*graphite_width
            spl_top = UnivariateSpline(xs, ys_top, s=0)
            spl_bottom = UnivariateSpline(xs, ys_bottom, s=0)
            spl_top_scaled = UnivariateSpline(xs, ys_top_scaled, s=0)
            spl_bottom_scaled = UnivariateSpline(xs, ys_bottom_scaled, s=0)
            area_top = graphite_thickness*graphite_width - spl_top.integral(0, graphite_width)
            area_bottom = spl_bottom.integral(0, graphite_width)
            area_top_scaled = graphite_thickness*graphite_width - spl_top_scaled.integral(0, graphite_width)
            area_bottom_scaled = spl_bottom_scaled.integral(0, graphite_width)
            area_PM_top = area_top_scaled - area_top
            area_PM_bottom = area_bottom_scaled - area_bottom
            # print((area_PM_top + area_PM_bottom)*1e-4)
            # print((area_bottom + area_top + v_putty_flat)*1e-4)
            v_added_sim = (area_bottom + area_top + v_putty_flat + (area_PM_top + area_PM_bottom)*(1-porosity))*1e-4
            if(np.abs(v_added_sim - v_added_meas) < 0.01*v_added_meas):
                values.append([scale, porosity, v_added_sim, v_added_meas, i])
                # print('scale', scale, 'porosity', porosity, 'sim', v_added_sim, 'meas', v_added_meas)
df_vals = pd.DataFrame(values, columns=['scale', 'porosity', 'v_added_sim', 'v_added_meas', 'file_index'])
df_vals = df_vals.sort_values(['file_index', 'scale'])
df_filt = df_vals[np.abs(df_vals['v_added_sim'] - df_vals['v_added_meas']) < 1e-8]
mapping = {}
for i in range(1000):
    mapping[i] = np.nan
for index, dxffile in enumerate(sorted((f for f in os.listdir('fusion add-in/generate_dxf/dxf_geometries') if not f.startswith(".")), key=str.lower)):
    mapping[index] = dxffile
df_filt['file_name'] = df_filt['file_index'].apply(lambda x: mapping[x])
df_filt.to_csv('depth_porosity_values_filt.csv', index=False)
