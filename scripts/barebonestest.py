import mph
import time
import numpy as np
import matplotlib.pyplot as plt

starttime = time.time()
print('starting client at ' + str(time.time() - starttime))
client = mph.start(cores=8)
print('loading model at ' + str(time.time() - starttime))
model = client.load('graphite-thermal-conductivity-2D.mph')
simtimes = []
print('solving model at ' + str(time.time() - starttime))
model.solve()
print('done at ' + str(time.time() - starttime))
