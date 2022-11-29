import mph
client = mph.start(cores=1)
model = client.load('graphite-thermal-conductivity.mph')
importNode = model/'geometries'/'Geometry 1'/'Import 1'

#list for the different spline points used in sketches
pts = ['10','20','30','40']
values = []

for i in pts:
    for x in range(5):
        importNode.property('filename','graphite_automated_split v1' + i +' pts' + str(x) +'.stp')
        model.build()
        model.mesh()
        model.solve()
        values.append(model.evaluate('bnd1'))

        print(values)

print(values)