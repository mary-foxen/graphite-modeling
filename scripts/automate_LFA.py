import numpy as np
import mph
import pandas as pd

client = mph.start(cores=1)
model = client.load('graphite-thermal-diffusivity-porous-2D.mph')
model.solve()
temp_t = model.evaluate('bnd1')
half_temp = model.evaluate('var1')
alpha_mean = model.evaluate('var3')[0]
(_, time) = model.inner('Study 1//Solution 1')
df = pd.DataFrame({'time': time, 'temp_t': temp_t, 'half_temp': half_temp})
time_half = df.loc[np.abs(df['temp_t'] - half_temp[0]).idxmin(), 'time']
total_t = float(model.parameters()['total_t'].split('[')[0])
app_alpha = 1.38*(total_t*1e-3)**2/np.pi**2/time_half
print('apparent alpha', app_alpha)
print('effective alpha', alpha_mean)
