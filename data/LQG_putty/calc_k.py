import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['science', 'grid'])

alpha_df_uncoated = pd.read_csv('graphite-putty samples/Thermal Diffusivity/5.csv', header=26)
alpha_df_uncoated = alpha_df_uncoated[alpha_df_uncoated['#Shot_number'] == '#Mean']
cp_df_g1 = pd.read_csv('graphite-putty samples/Specific Heat/Graphite/sample1.csv', header=34)
cp_df_g1 = cp_df_g1[cp_df_g1['##Temp./C'] > 200]
cp_df_g2 = pd.read_csv('graphite-putty samples/Specific Heat/Graphite/sample2.csv', header=34)
cp_df_g2 = cp_df_g2[cp_df_g2['##Temp./C'] > 200]
cp_df_g3 = pd.read_csv('graphite-putty samples/Specific Heat/Graphite/sample3.csv', header=34)
cp_df_g3 = cp_df_g3[cp_df_g3['##Temp./C'] > 200]
temps = np.arange(200, 500, 10)
data = []
for i in temps:
    df_temp_1 = cp_df_g1[np.abs(cp_df_g1['##Temp./C'] - i) < 5]
    avg_cp_1 = np.mean(df_temp_1['Cp(5)/(J/(g*K))'])
    df_temp_2 = cp_df_g2[np.abs(cp_df_g2['##Temp./C'] - i) < 5]
    avg_cp_2 = np.mean(df_temp_2['Cp(5)/(J/(g*K))'])
    df_temp_3 = cp_df_g3[np.abs(cp_df_g3['##Temp./C'] - i) < 5]
    avg_cp_3 = np.mean(df_temp_3['Cp(5)/(J/(g*K))'])
    avg_cp = np.mean([avg_cp_1, avg_cp_2, avg_cp_3])
    min_cp = np.min([avg_cp_1, avg_cp_2, avg_cp_3])
    max_cp = np.max([avg_cp_1, avg_cp_2, avg_cp_3])
    data.append([i, avg_cp_1, avg_cp_2, avg_cp_3, avg_cp, min_cp, max_cp])
cp_df_g = pd.DataFrame(data, columns=['T', 'cp1', 'cp2', 'cp3', 'cp_avg', 'cp_min', 'cp_max'])
cp_df_g.to_csv('graphite-putty samples/Specific Heat/Graphite/avg_cp.csv', index=False)

alpha_df_putty1 = pd.read_csv('graphite-putty samples/Thermal Diffusivity/P1.csv', header=26)
alpha_df_putty1 = alpha_df_putty1[alpha_df_putty1['#Shot_number'] == '#Mean']
# alpha_df_putty1 = alpha_df_putty1[alpha_df_putty1['#Temperature/C'] < 300]
alpha_df_putty2 = pd.read_csv('graphite-putty samples/Thermal Diffusivity/P2.csv', header=26)
alpha_df_putty2 = alpha_df_putty2[alpha_df_putty2['#Shot_number'] == '#Mean']
# alpha_df_putty2 = alpha_df_putty2[alpha_df_putty2['#Temperature/C'] < 300]
alpha_df_putty3 = pd.read_csv('graphite-putty samples/Thermal Diffusivity/P3.csv', header=26)
alpha_df_putty3 = alpha_df_putty3[alpha_df_putty3['#Shot_number'] == '#Mean']
# alpha_df_putty3 = alpha_df_putty3[alpha_df_putty3['#Temperature/C'] < 300]
temps = np.arange(20, 1200, 10)
data = []
for i in temps:
    df_temp_1 = alpha_df_putty1[alpha_df_putty1['#Temperature/C'] == i]
    avg_alpha_1 = np.mean(df_temp_1['#Diffusivity/(mm^2/s)'])
    df_temp_2 = alpha_df_putty2[alpha_df_putty2['#Temperature/C'] == i]
    avg_alpha_2 = np.mean(df_temp_2['#Diffusivity/(mm^2/s)'])
    df_temp_3 = alpha_df_putty3[alpha_df_putty3['#Temperature/C'] == i]
    avg_alpha_3 = np.mean(df_temp_3['#Diffusivity/(mm^2/s)'])
    avg_alpha = np.mean([avg_alpha_1, avg_alpha_2, avg_alpha_3])
    data.append([i, avg_alpha_1, avg_alpha_2, avg_alpha_3, avg_alpha])
alpha_df_putty = pd.DataFrame(data, columns=['T', 'alpha1', 'alpha2', 'alpha3', 'alpha_avg'])
alpha_df_putty['min'] = alpha_df_putty[['alpha1', 'alpha2', 'alpha3']].min(axis=1)
alpha_df_putty['max'] = alpha_df_putty[['alpha1', 'alpha2', 'alpha3']].max(axis=1)
alpha_df_putty.dropna(inplace=True)
alpha_df_putty.to_csv('graphite-putty samples/Thermal Diffusivity/avg_alpha_putty.csv', index=False)

cp_df_p1 = pd.read_csv('graphite-putty samples/Specific Heat/Putty/sample1.csv', header=34)
# cp_df_p1 = cp_df_p1[cp_df_p1['##Temp./C']]


def rho_T(T):
    return 1.6 - 0.000025 * T


def rho_T_alpha(T):
    return 1.4 - 0.000025 * T


def cp_T(T):
    # fit from matlab for cp from 200C to 500C using same form as literature fit
    # a = 1.597
    # b = 0.0002746
    # c = -117.8
    # d = -0.2472
    # e = 0.7528
    # f = 0.276
    T = T+273
    # a = 2.126
    # b = 0
    # c = -481.5
    # d = -0.6239
    # e = 0.9443
    # f = 0.4909
    # g = 0.4893
    a = 2.208
    b = 1.838e-07
    c = -508.9
    d = -2.476
    e = 0.8138
    f = 0.6935
    g = 0.3171
    cp_lit_fit2 = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0)
    return cp_lit_fit2


def cp_lit(T):
    T = T + 273.15
    return (0.538657 + 9.11129e-6*T - 90.2725*T**(-1.0) - 43449.3*T**(-2.0) + 1.59309e7*T**(-3.0) - 1.43688e9*T**(-4.0))*4.184


def alpha_T(T):
    T = T+273
    a = 2.187
    b = 0.0003048
    c = 2688
    d = 13.66
    e = 0.1724
    f = 0.9421
    g = 0.9561
    alpha_fit = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0)
    return alpha_fit


def alpha_T_5(T):
    T = T+273
    a = 3.515
    b = -0.001538
    c = 1267
    d = 7.744
    e = 0.9632
    k = 4.142e-13
    alpha_fit = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + k*T**4
    return alpha_fit

def k_putty_old(T):
    # a = 1.801
    # b = 5.564e-05
    # c = -14.43
    # d = 20.44
    # e = 1.366
    # f = 0.9919
    # g = 0.5472
    # k_fit = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0)
    # return k_fit
    pass

def k_putty(T):
    T = T+273
    a = 82.91
    b = -0.2536
    c = -9305
    d = -85.61
    e = 0.9887
    f = 0.6456
    g = 0.4795
    h = 0.6393
    k = 0.0003402
    l = -1.854e-07
    m = 3.549e-11
    k_fit = a + b*T + c*T **(-1.0) + d*T ** (-2.0) + e*T**(-3.0) + f*T**(-4.0) + g * \
        T**(-5.0) + h*T**(-6.0) + k*T**2 + l*T**3 + m*T**4
    return k_fit


T_alpha = alpha_df_uncoated['#Temperature/C']
alpha = alpha_df_uncoated['#Diffusivity/(mm^2/s)']
# alpha_fit = np.polyfit(T_alpha, alpha, 5)
fig = plt.figure(num=1, clear=True)
plt.plot(T_alpha, alpha, 'ro', label='Thermal Diffusivity', markerfacecolor='none', markersize=4)
plt.plot(T_alpha, alpha_T_5(T_alpha), 'b', label='Thermal Diffusivity Fit', zorder=10)
# # plt.plot(T_alpha, np.polyval(alpha_fit, T_alpha), label='Thermal Diffusivity Fit')
# plt.plot(T_alpha, alpha_T(T_alpha), label='Thermal Diffusivity Fit')
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Diffusivity (mm$^2$/s)')
plt.legend()
# plt.grid()
plt.tight_layout()
plt.savefig('plots/alpha_5.pdf')

fig = plt.figure(num=1, clear=True)
for val in ['3', '2', '8']:
    alpha_df = pd.read_csv('graphite-putty samples/Thermal Diffusivity/'+val+'.csv', header=26)
    alpha_df = alpha_df[alpha_df['#Shot_number'] == '#Mean']
    alpha_df.to_csv('graphite-putty samples/Thermal_Diffusivity/'+val+'_mean.csv', index=False)
    T_alpha = alpha_df['#Temperature/C']
    alpha = alpha_df['#Diffusivity/(mm^2/s)']
    # alpha_fit = np.polyfit(T_alpha, alpha, 5)
    plt.plot(T_alpha, alpha, '.-', label='Sample '+val, markerfacecolor='none', markersize=4)
    # plt.plot(T_alpha, alpha_T_5(T_alpha), 'b', label='Thermal Diffusivity Fit', zorder=10)
    # # plt.plot(T_alpha, np.polyval(alpha_fit, T_alpha), label='Thermal Diffusivity Fit')
    # plt.plot(T_alpha, alpha_T(T_alpha), label='Thermal Diffusivity Fit')
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Diffusivity (mm$^2$/s)')
plt.legend()
# plt.grid()
plt.tight_layout()
plt.savefig('plots/alpha_coated.pdf')

# # T = T_alpha + 273.15
# # T = 300
# # cp_lit = (0.630375 - 1.60535e-5*T - 225.861 *
# #           T**(-1.0) + 3100.1*T**(-2.0) - 910737*T**(-3.0) - 9.64607e7*T**(-4.0))*4.184

T_cp_fit = np.linspace(200, 2500, 100)
# T_k = np.linspace(200, 2500, 1000)
fig = plt.figure(num=2, clear=True)
# T_cp1 = cp_df_g1['##Temp./C']
# cp1 = cp_df_g1['Cp(5)/(J/(g*K))']
# T_cp2 = cp_df_g2['##Temp./C']
# cp2 = cp_df_g2['Cp(5)/(J/(g*K))']
# T_cp3 = cp_df_g3['##Temp./C']
# cp3 = cp_df_g3['Cp(5)/(J/(g*K))']
T_cp = cp_df_g['T']
cp1 = cp_df_g['cp1']
cp2 = cp_df_g['cp2']
cp3 = cp_df_g['cp3']
cp_avg = cp_df_g['cp_avg']
cp_min = cp_df_g['cp_min']
cp_max = cp_df_g['cp_max']
plt.plot(T_cp, cp1, '.-',  label='Sample C1')
plt.plot(T_cp, cp2, '.-',  label='Sample C2')
plt.plot(T_cp, cp3, '.-',  label='Sample C3')
plt.legend()
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Specific Heat (J/gK)')
plt.tight_layout()
plt.savefig('plots/cp_5_samples.pdf')

plt.figure(num=2, clear=True)
plt.plot(T_cp, cp_avg, 'ro', markerfacecolor='none', label='Specific Heat Avg')
plt.fill_between(T_cp, cp_min, cp_max, alpha=0.25, color='r')
# plt.errorbar(T_cp, cp_avg, yerr=[cp_avg-cp_min, cp_max-cp_avg], fmt='none', ecolor='r', capsize=2, label='Specific Heat Range')
# # plt.plot(T_k, np.polyval(cp_fit, T_k), 'b', label='Specific Heat Fit')
plt.plot(T_cp_fit, cp_T(T_cp_fit), 'b-', label='Specific Heat Fit')
plt.plot(T_cp_fit, cp_lit(T_cp_fit), 'k--', label='Specific Heat Literature')
# # plt.plot(T_alpha, np.polyval(cp_fit_lit, T_alpha), '--', label='Specific Heat Literature Fit')
plt.legend()
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Specific Heat (J/gK)')
plt.tight_layout()
plt.savefig('plots/cp_5.pdf')

# fig = plt.figure(num=4, clear=True)
# plt.plot(T_k, rho_T(T_k), 'b', label='Density')
# plt.xlabel('Temperature (C)')
# plt.ylabel('Density (g/cm^3)')
# plt.grid()
# plt.savefig('rho_fit.png')

# cp_df = cp_df[:11]
# k = cp_df['AvgSpeciHeat_J_gK'] * cp_df['AvgThermDiff_mm2_s'] * rho_T(cp_df['Temperature_C'])
# k_fit = rho_T(T_k) * cp_T(T_k) * alpha_T(T_k)
k = alpha_df_uncoated['#Diffusivity/(mm^2/s)'] * cp_T(T_alpha) * rho_T(T_alpha)
T_k = np.linspace(25, 2000, 1000)
k_fit = alpha_T_5(T_k) * cp_T(T_k) * rho_T(T_k)
k_df = pd.DataFrame({'T': T_alpha, 'k': k})
k_df.to_csv('k_5.csv', index=False)
fig = plt.figure(num=3, clear=True)
plt.plot(T_alpha, k, 'ro-', markerfacecolor='none', markersize=4, label='Measured')
plt.plot(T_k, k_fit, 'b', label='Fit and Extrapolation')
# plt.plot(T_k, k_fit, 'b', label='Thermal Conductivity')
# plt.grid()
plt.legend()
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Conductivity (W/mK)')
plt.tight_layout()
plt.savefig('plots/k_5.pdf')

fig = plt.figure(num=4, clear=True)
plt.plot(alpha_df_putty1['#Temperature/C'], alpha_df_putty1['#Diffusivity/(mm^2/s)'],
         'o-', label='Sample 1')
plt.plot(alpha_df_putty2['#Temperature/C'], alpha_df_putty2['#Diffusivity/(mm^2/s)'],
         'o-', label='Sample 2')
plt.plot(alpha_df_putty3['#Temperature/C'], alpha_df_putty3['#Diffusivity/(mm^2/s)'],
         'o-', label='Sample 3')
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Diffusivity (mm$^2$/s)')
plt.legend()
plt.tight_layout()
plt.savefig('plots/alpha_putty_samples.pdf')

fig = plt.figure(num=4, clear=True)
plt.plot(alpha_df_putty['T'], alpha_df_putty['alpha_avg'], 'ro-', label='Average thermal diffusivity')
plt.fill_between(alpha_df_putty['T'], alpha_df_putty['min'], alpha_df_putty['max'], color='r', alpha=0.25)
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Diffusivity (mm$^2$/s)')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('plots/alpha_putty.pdf')


fig = plt.figure(num=5, clear=True)
T_cp_fit = np.linspace(min(cp_df_p1['##Temp./C']), max(cp_df_p1['##Temp./C']), 100)
cp_df_p1 = cp_df_p1[cp_df_p1['##Temp./C'] < 250]
plt.plot(cp_df_p1['##Temp./C'], cp_df_p1['Cp(1)/(J/(g*K))'], 'ro',
         label='Specific Heat 1', markerfacecolor='none', markersize=4)
plt.plot(T_cp_fit, cp_lit(T_cp_fit)*1.5, 'b-', label='Specific Heat Fit')
plt.plot(T_cp_fit, cp_lit(T_cp_fit), 'k--', label='Specific Heat Literature')
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Specific Heat (J/gK)')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig('plots/cp_putty.pdf')

fig = plt.figure(num=6, clear=True)
# alpha_df_putty = alpha_df_putty[alpha_df_putty['T'] < 250][alpha_df_putty['T'] > 90]
avg_k = alpha_df_putty['alpha_avg'] * cp_lit(alpha_df_putty['T']) * 1.5 * rho_T_alpha(alpha_df_putty['T'])
min_k = alpha_df_putty['min'] * cp_lit(alpha_df_putty['T']) * 1.5 * rho_T_alpha(alpha_df_putty['T'])
max_k = alpha_df_putty['max'] * cp_lit(alpha_df_putty['T']) * 1.5 * rho_T_alpha(alpha_df_putty['T'])
alpha_df_putty['k_avg'] = avg_k
alpha_df_putty.to_csv('graphite-putty samples/Thermal Diffusivity/avg_alpha_putty.csv', index=False)
# plt.plot(alpha_df_putty1['#Temperature/C'], k1, 'o-', label='Thermal Conductivity 1')
# plt.plot(alpha_df_putty2['#Temperature/C'], k2, 'o-', label='Thermal Conductivity 2')
# plt.plot(alpha_df_putty3['#Temperature/C'], k3, 'o-', label='Thermal Conductivity 3')
T_k = np.linspace(25, 1200, 100)
plt.plot(alpha_df_putty['T'], avg_k, 'ro', label='Average k')
plt.fill_between(alpha_df_putty['T'], min_k, max_k, color='r', alpha=0.25)
plt.plot(T_k, k_putty(T_k), 'b-', label='Fit')
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Conductivity (W/mK)')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig('plots/k_putty.pdf')

plt.show()
