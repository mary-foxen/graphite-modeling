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
for i in range(50):
    print('loading model at ' + str(time.time() - starttime))
    model = client.load('graphite-thermal-conductivity-2D.mph')
    beginsim = time.time()
    print('solving model at ' + str(time.time() - starttime))
    model.solve()
    print('done at ' + str(time.time() - starttime))
    donesim = time.time() - beginsim
    simtimes.append(donesim)

print(np.mean(simtimes))
plt.figure(num=1, clear=True)
plt.plot(simtimes)
plt.title('runtime vs. iteration')
plt.savefig('simtimes_reload.png')

simtimes = []
for i in range(50):
    beginsim = time.time()
    print('solving model at ' + str(time.time() - starttime))
    model.solve()
    print('done at ' + str(time.time() - starttime))
    donesim = time.time() - beginsim
    simtimes.append(donesim)

print(np.mean(simtimes))
plt.figure(num=1, clear=True)
plt.plot(simtimes)
plt.title('runtime vs. iteration')
plt.savefig('simtimes.png')
plt.show()
