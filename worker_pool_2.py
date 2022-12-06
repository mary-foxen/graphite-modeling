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
    model.solve('Study 1')
    k = model.evaluate('bnd1')
    return np.atleast_1d(k)[0]


def boss():
    values = []
    for fileName in os.listdir('fusion add-in'):
        if os.path.splitext(fileName)[1] == '.dxf':
            values.append('fusion add-in/'+fileName)
    print('initializing')
    the_pool = multiprocessing.Pool(min(len(values), os.cpu_count()), worker_init, (worker_main,))
    all_res = [the_pool.apply_async(worker_main, (role,)) for role in values]
    print('running')
    ks = [res.get() for res in tqdm(all_res)]
    print(ks)


if __name__ == '__main__':
    boss()
