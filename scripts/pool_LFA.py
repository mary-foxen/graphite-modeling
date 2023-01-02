import os
import time
import multiprocessing
import mph
import numpy as np
import pandas as pd
from matplotlib import pyplot
from tqdm import tqdm


def worker_init(function):
    """Performs jobs and delivers the results."""
    mph.option('session', 'stand-alone')
    client = mph.start(cores=1)
    model = client.load('graphite-thermal-diffusivity-porous-2D.mph')
    function.model = model


def worker_main(d):
    model = worker_main.model
    importNode = model/'geometries'/'Geometry 1'/'Import 1'
    importNode.property('filename', str(d))
    total_t = 4
    model.parameter('total_t', str(total_t)+'[mm]')
    model.solve('Study 1')
    temp_t = model.evaluate('bnd1')
    half_temp = model.evaluate('var1')
    alpha_mean = model.evaluate('var3')
    (_, time) = model.inner('Study 1//Solution 1')
    df = pd.DataFrame({'time': time, 'temp_t': temp_t, 'half_temp': half_temp})
    time_half = df.loc[np.abs(df['temp_t'] - half_temp[0]).idxmin(), 'time']
    alpha_app = 1.38*(total_t*1e-3)**2/np.pi**2/time_half
    return alpha_app, alpha_mean, d


def boss():
    values = []
    for fileName in sorted(os.listdir('geometries')):
        if os.path.splitext(fileName)[1] == '.dxf':
            values.append('geometries/'+fileName)
    print('initializing')
    the_pool = multiprocessing.Pool(min(len(values), int(os.cpu_count()/2)), worker_init, (worker_main,))
    all_res = [the_pool.apply_async(worker_main, (role,)) for role in values]
    print('running')
    # all_res = the_pool.map_async(worker_main, values)
    ks = [res.get() for res in tqdm(all_res)]
    df = pd.DataFrame(ks, columns=['alpha_app', 'alpha_mean', 'file'])
    df = df.sort_values('file')
    df.to_csv('alpha.csv', index=False)
    # print(ks)
    # print(min(ks), max(ks))


if __name__ == '__main__':
    boss()
