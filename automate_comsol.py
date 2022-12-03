import mph
import pandas as pd
import numpy as np


# mph.option('stand-alone')
print('starting client')
client = mph.start(cores=4)
print('loading model')
model = client.load('graphite-thermal-conductivity-2D.mph')
importNode = model/'geometries'/'Geometry 1'/'Import 1'

values = []

print('reading csv')
df = pd.read_csv("fusion add-in/data.csv")
files = df.loc[:, "filename"]
for f in files:
    print('setting filename')
    importNode.property('filename', str(f))
    print('building model')
    model.build()
    print('meshing model')
    model.mesh()
    print('solving model')
    model.solve()
    print('evaluating effective k')
    values.append(np.atleast_1d(model.evaluate('bnd1'))[0])
    print(values)


# Using 'eff_k' as the column name
# and equating it to the list values
df['eff_k'] = values

# save back to data.csv file
df.to_csv("comsol_data.csv", index=False)

print(df)
