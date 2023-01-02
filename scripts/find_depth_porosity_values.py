import numpy as np
import mph
import pandas as pd
from tqdm import tqdm

client = mph.start(cores=1)
model = client.load('graphite-geometry-porous-2D-20pts.mph')
values = []
for scale in tqdm(np.linspace(0.41, 0.99, 100)):
    porosity = 0.41/scale
    model.parameter('pm_scale', scale)
    model.parameter('v1', porosity)
    model.build()
    model.mesh()
    model.solve()
    v_added_sim = model.evaluate('var4')
    v_added_meas = model.evaluate('var5')
    print('scale', scale, 'porosity', porosity, 'sim', v_added_sim, 'meas', v_added_meas)
    if(np.abs(v_added_sim - v_added_meas) < 0.01*v_added_meas):
        values.append([scale, porosity, v_added_sim, v_added_meas])
df = pd.DataFrame(values, columns=['scale', 'porosity', 'v_added_sim', 'v_added_meas'])
df.to_csv('depth_porosity_values.csv', index=False)
