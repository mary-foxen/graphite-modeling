import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use(['science', 'grid'])


# for depth in putty_depths:
#     k_depth = k_data[k_data['depth'] == depth]
#     print(depth, np.min(k_depth['k']), np.mean(k_depth['k']), np.max(k_depth['k']))


def series_approx_simple():
    v_putty = (total_thickness - graphite_thickness)/total_thickness
    v_graphite = graphite_thickness/total_thickness
    k_eff = 1/(v_putty/k_putty + v_graphite/k_graphite)
    print('k_eff', k_eff)


def series_approx_incl_inside():
    v_putty = (total_thickness - graphite_thickness + vol_inside)/total_thickness
    v_graphite = (graphite_thickness-vol_inside)/total_thickness
    k_eff = 1/(v_putty/k_putty + v_graphite/k_graphite)
    # print('k_eff', k_eff)
    return k_eff


def series_parallel():
    scaling_v_inside = 1.05
    L_putty_top = (total_thickness - graphite_thickness)/2
    L_parallel_top = vol_inside/2*scaling_v_inside
    L_graphite = graphite_thickness - vol_inside*scaling_v_inside
    L_parallel_bottom = vol_inside/2*scaling_v_inside
    L_putty_bottom = (total_thickness - graphite_thickness)/2
    L_total = L_putty_top + L_parallel_top + L_graphite + L_parallel_bottom + L_putty_bottom
    R1 = L_putty_top/k_putty
    v_vol_inside_putty = 1/scaling_v_inside
    k2 = v_vol_inside_putty*k_putty + (1-v_vol_inside_putty)*k_graphite
    R2 = L_parallel_top/k2
    R3 = L_graphite/k_graphite
    k3 = v_vol_inside_putty*k_putty + (1-v_vol_inside_putty)*k_graphite
    R4 = L_parallel_bottom/k3
    R5 = L_putty_bottom/k_putty
    R_total = R1 + R2 + R3 + R4 + R5
    k_eff = L_total/R_total
    # print('k_eff', k_eff)
    return k_eff


def get_porosity_from_scale(x):

    p1 = -2.491192543245683e+03
    p2 = 1.054501333968927e+04
    p3 = -1.890692698527842e+04
    p4 = 1.867707055121285e+04
    p5 = -1.107877479811161e+04
    p6 = 4.034624546195068e+03
    p7 = -8.859448117678304e+02
    p8 = 1.104928612838191e+02
    p9 = -7.002779605942499
    p10 = 1.111863835040044

    df = pd.read_csv('depth_porosity_values_filt.csv')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    xs = np.linspace(0, 1, 100)
    y = p1*xs**9 + p2*xs**8 + p3*xs**7 + p4*xs**6 + p5*xs**5 + p6*xs**4 + p7*xs**3 + p8*xs**2 + p9*xs + p10
    plt.plot(df['scale'], df['porosity'], '.')
    plt.plot(xs, y, '-')
    plt.xlabel('scale')
    plt.ylabel('porosity')
    plt.grid()
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    ax.set_aspect('equal')
    plt.show()

    porosity = p1*x**9 + p2*x**8 + p3*x**7 + p4*x**6 + p5*x**5 + p6*x**4 + p7*x**3 + p8*x**2 + p9*x + p10

    return porosity


def series_parallel_permeable():
    scaling_v_inside = 1.05
    scaling_EMT = 0.6
    L_putty_top = (total_thickness - graphite_thickness)/2
    L_parallel_top = vol_inside/2*scaling_v_inside
    L_EMT_top = graphite_thickness*scaling_EMT/2
    L_graphite = graphite_thickness - vol_inside*scaling_v_inside - graphite_thickness*scaling_EMT
    scale_graphite = L_graphite/graphite_thickness
    print('scale_graphite', scale_graphite)
    v_graphite = get_porosity_from_scale(scale_graphite)
    v_putty = 1-v_graphite
    print('v_graphite', v_graphite)
    print('v_putty', v_putty)
    L_EMT_bottom = graphite_thickness*scaling_EMT/2
    L_parallel_bottom = vol_inside/2*scaling_v_inside
    L_putty_bottom = (total_thickness - graphite_thickness)/2
    L_total = L_putty_top + L_parallel_top + L_EMT_top + L_graphite + L_EMT_bottom + L_parallel_bottom + L_putty_bottom
    R1 = L_putty_top/k_putty
    v_vol_inside_putty = 1/scaling_v_inside
    k2 = v_vol_inside_putty*k_putty + (1-v_vol_inside_putty)*k_graphite
    R2 = L_parallel_top/k2
    k3 = (k_graphite*v_graphite + k_putty*v_putty*(3*k_graphite)/(2*k_graphite + k_putty)) / \
        (v_graphite + v_putty*(3*k_graphite)/(2*k_graphite + k_putty))
    R3 = L_EMT_top/k3
    R4 = L_graphite/k_graphite
    k5 = (k_graphite*v_graphite + k_putty*v_putty*(3*k_graphite)/(2*k_graphite + k_putty)) / \
        (v_graphite + v_putty*(3*k_graphite)/(2*k_graphite + k_putty))
    R5 = L_EMT_bottom/k5
    k6 = v_vol_inside_putty*k_putty + (1-v_vol_inside_putty)*k_graphite
    R6 = L_parallel_bottom/k6
    R7 = L_putty_bottom/k_putty
    R_total = R1 + R2 + R3 + R4 + R5 + R6 + R7
    k_eff = L_total/R_total
    print('k_eff', k_eff)


graphite_width = 1
graphite_thickness = 0.3  # measured

# vol_final = graphite_thickness*graphite_width*(1.05)  # measured

# putty_depths = [0.03, 0.04, 0.05, 0.06]
# num_spline_points = [10, 20]
# print('vol_init', vol_init)
# print('vol_final', vol_final)
# print('total_thickness', total_thickness)
# print('vol_inside', vol_inside)
k_putty = 2
k_graphite = 10
print('nonpermeable data')
# total_t = vol_final*10
k_data_comp = []
for total_t in np.linspace(3.01, 4, 20):
    vol_init = graphite_thickness*graphite_width*0.9  # measured
    vol_final = total_t/10
    full_vol_init = graphite_thickness * graphite_width
    vol_inside = full_vol_init - vol_init
    vol_outside = vol_final - full_vol_init
    total_thickness = vol_final / graphite_width  # check against measured
    putty_area = vol_inside
    k_data = pd.read_csv('k_nonperm_data/k_nonperm_%0.2e.csv' % total_t)
    k_data['depth'] = [float(res.split('_')[3]) for res in k_data['file']]
    min_k = np.min(k_data['k'])
    mean_k = np.mean(k_data['k'])
    max_k = np.max(k_data['k'])
    k_eff = series_parallel()
    k_eff_series = series_approx_incl_inside()
    k_data_comp.append([total_t, min_k, mean_k, max_k, k_eff, k_eff_series])
    # print(np.min(k_data['k']), np.mean(k_data['k']), np.max(k_data['k']))

k_data_comp_df = pd.DataFrame(k_data_comp, columns=['total_t', 'min_k', 'mean_k', 'max_k', 'k_eff', 'k_eff_series'])

fig = plt.figure(num=1, clear=True)
ax = fig.add_subplot(111)
plt.plot(k_data_comp_df['total_t'], k_data_comp_df['mean_k'], 'ro', label='data')
plt.plot(k_data_comp_df['total_t'], k_data_comp_df['k_eff'], 'b-', label='5-layer model')
plt.plot(k_data_comp_df['total_t'], k_data_comp_df['k_eff_series'], 'b--', label='3-layer model')
plt.fill_between(k_data_comp_df['total_t'], k_data_comp_df['min_k'], k_data_comp_df['max_k'], color='r', alpha=0.25)
plt.xlabel('total thickness (mm)')
plt.ylabel('k (W/mK)')
plt.ylim(4,8)
plt.legend()
plt.tight_layout()
plt.savefig('eff_k_EMT.pdf')
# plt.show()

k_data_comp = []
total_t = 3.15
for scale in np.linspace(1, 2, 10):
    perc_putty = 0.1*scale
    vol_init = graphite_thickness*graphite_width*(1-perc_putty)  # measured
    vol_final = total_t/10
    full_vol_init = graphite_thickness * graphite_width
    vol_inside = full_vol_init - vol_init
    vol_outside = vol_final - full_vol_init
    total_thickness = vol_final / graphite_width  # check against measured
    putty_area = vol_inside
    k_data = pd.read_csv('k_nonperm_data/k_nonperm_%0.2e_%0.2e.csv' % (total_t, scale))
    k_data['depth'] = [float(res.split('_')[3]) for res in k_data['file']]
    min_k = np.min(k_data['k'])
    mean_k = np.mean(k_data['k'])
    max_k = np.max(k_data['k'])
    k_eff = series_parallel()
    k_eff_series = series_approx_incl_inside()
    k_data_comp.append([total_t, perc_putty, min_k, mean_k, max_k, k_eff, k_eff_series])
    # print(np.min(k_data['k']), np.mean(k_data['k']), np.max(k_data['k']))

k_data_comp_df = pd.DataFrame(k_data_comp, columns=['total_t', 'scale', 'min_k', 'mean_k', 'max_k', 'k_eff', 'k_eff_series'])

fig = plt.figure(num=2, clear=True)
ax = fig.add_subplot(111)
plt.plot(k_data_comp_df['scale'], k_data_comp_df['mean_k'], 'ro', label='data')
plt.plot(k_data_comp_df['scale'], k_data_comp_df['k_eff'], 'b-', label='5-layer model')
plt.plot(k_data_comp_df['scale'], k_data_comp_df['k_eff_series'], 'b--', label='3-layer model')
plt.fill_between(k_data_comp_df['scale'], k_data_comp_df['min_k'], k_data_comp_df['max_k'], color='r', alpha=0.25)
plt.xlabel('frac putty in initial volume')
plt.ylabel('k (W/mK)')
plt.ylim(4,8)
plt.legend()
plt.tight_layout()
plt.savefig('eff_k_EMT_2.pdf')
# plt.show()

k_data_comp = []
for total_t in np.linspace(3.01, 4, 10):
    for scale in np.linspace(0.1,5,10):
        perc_putty = 0.1*scale
        vol_init = graphite_thickness*graphite_width*(1-perc_putty)  # measured
        vol_final = total_t/10
        full_vol_init = graphite_thickness * graphite_width
        vol_inside = full_vol_init - vol_init
        vol_outside = vol_final - full_vol_init
        total_thickness = vol_final / graphite_width  # check against measured
        putty_area = vol_inside
        k_data = pd.read_csv('k_nonperm_data/k_nonperm_%0.2e_%0.2e.csv' % (total_t, scale))
        k_data['depth'] = [float(res.split('_')[3]) for res in k_data['file']]
        min_k = np.min(k_data['k'])
        mean_k = np.mean(k_data['k'])
        max_k = np.max(k_data['k'])
        k_eff = series_parallel()
        k_data_comp.append([total_t, perc_putty, min_k, mean_k, max_k, k_eff])

k_data_comp_df = pd.DataFrame(k_data_comp, columns=['total_t', 'scale', 'min_k', 'mean_k', 'max_k', 'k_eff'])

fig = plt.figure(num=3, clear=True)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(k_data_comp_df['total_t'], k_data_comp_df['scale'], k_data_comp_df['mean_k'], c='r', label='data')
ax.scatter(k_data_comp_df['total_t'], k_data_comp_df['scale'], k_data_comp_df['k_eff'], c='b', label='model')
ax.set_xlabel('total thickness (mm)')
ax.set_ylabel('frac putty in initial volume')
ax.set_zlabel('k (W/mK)')
plt.legend()
plt.tight_layout()
plt.savefig('eff_k_EMT_3.pdf')
plt.show()

# print('EMT data')
# series_approx_simple()
# series_approx_incl_inside()
# series_parallel()

# print('permeable data')
# k_data = pd.read_csv('k.csv')
# k_data['depth'] = [float(res.split('_')[3]) for res in k_data['file']]
# print(np.min(k_data['k']), np.mean(k_data['k']), np.max(k_data['k']))

# print('EMT_data')
# series_parallel_permeable()
