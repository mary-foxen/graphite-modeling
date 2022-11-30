import mph
import pandas as pd

client = mph.start(cores=1)
model = client.load('graphite-thermal-conductivity.mph')
importNode = model/'geometries'/'Geometry 1'/'Import 1'

values = []


df = pd.read_csv("data.csv")
files = df.loc[:,"filename"]
for f in files:
    importNode.property('filename', str(f))
    model.build()
    model.mesh()
    model.solve()
    values.append(model.evaluate('bnd1'))


# Using 'eff_k' as the column name
# and equating it to the list values
df['eff_k'] = values

print(df)

