import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

graphite_width = 1
graphite_thickness = 0.3
putty_depths = [0.03, 0.04, 0.05, 0.06]
vol_init = graphite_thickness*graphite_width*0.9
vol_final = graphite_thickness*graphite_width*1.1
full_vol_init = graphite_thickness * graphite_width
vol_inside = full_vol_init - vol_init
total_thickness = vol_final / graphite_width
vol_outside = (total_thickness*graphite_width) - (graphite_thickness*graphite_width)
putty_area = vol_inside
num_spline_points = [10, 20]

all_xs = []
all_ys_bottom = []
all_ys_top = []
all_num_points = []
all_putty_depths = []

for putty_depth in putty_depths:
    for num in num_spline_points:  # traces through num_spline_points to generate different porosities
        numGeom = 0
        totNumGeom = 20
        with tqdm(total=totNumGeom) as pbar:
            while numGeom < totNumGeom:
                startRange = 0  # Start of range to be evaluated.
                endRange = graphite_width  # End of range to be evaluated.
                splinePoints = num  # Number of points that splines are generated.
                i = 1
                xs = [0]
                ys_bottom = [0]
                ys_top = [graphite_thickness]
                while i <= (splinePoints-1):
                    t = startRange + ((endRange - startRange)/splinePoints)*i
                    xCoord = t
                    yCoord_bottom = np.random.uniform(0, putty_depth)
                    yCoord_top = np.random.uniform(graphite_thickness - putty_depth, graphite_thickness)
                    zCoord = 0
                    xs.append(xCoord)
                    ys_bottom.append(yCoord_bottom)
                    ys_top.append(yCoord_top)
                    i = i + 1
                ys_bottom.append(0)
                ys_top.append(graphite_thickness)
                xs.append(graphite_width)
                spl_top = UnivariateSpline(xs, ys_top, s=0)
                spl_bottom = UnivariateSpline(xs, ys_bottom, s=0)
                area_top = graphite_thickness*graphite_width - spl_top.integral(0, graphite_width)
                area_bottom = spl_bottom.integral(0, graphite_width)
                x_new = np.linspace(0, graphite_width, 1000)

                if np.abs((area_bottom+area_top)-putty_area) < 0.01*putty_area and \
                        max(ys_bottom) > (putty_depth*0.9) and min(ys_top) < (graphite_thickness - putty_depth*0.9):
                    all_xs.append(xs)
                    all_ys_bottom.append(ys_bottom)
                    all_ys_top.append(ys_top)
                    all_num_points.append(num)
                    all_putty_depths.append(putty_depth)
                    numGeom += 1
                    pbar.update(1)
                    # plt.plot(xs, ys_top, 'o', x_new, spl_top(x_new), '-')
                    # plt.plot(xs, ys_bottom, 'o', x_new, spl_bottom(x_new), '-')
                    # plt.show()
                    # print(area_top+area_bottom, putty_area)
                else:
                    continue

            df = pd.DataFrame({'xs': all_xs, 'ys_bottom': all_ys_bottom, 'ys_top': all_ys_top,
                               'num_points': all_num_points, 'putty_depth': all_putty_depths})

            df.to_csv('graphite_points.csv', index=False)
