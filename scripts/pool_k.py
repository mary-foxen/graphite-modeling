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
    model = client.load('graphite-thermal-conductivity-2D.mph')
    function.model = model


def worker_main(d):
    model = worker_main.model
    importNode = model/'geometries'/'Geometry 1'/'Import 1'
    importNode.property('filename', str(d))
    model.parameter('total_t', '4[mm]')
    model.solve('Study 1')
    k = model.evaluate('bnd1')
    return np.atleast_1d(k)[0], d


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
    df = pd.DataFrame(ks, columns=['k', 'file'])
    df = df.sort_values('file')
    df.to_csv('k.csv', index=False)
    # print(ks)
    # print(min(ks), max(ks))


if __name__ == '__main__':
    boss()
