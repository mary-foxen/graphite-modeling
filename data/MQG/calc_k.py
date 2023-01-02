import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['science', 'grid'])
alpha_df = pd.read_csv('thermal diffusivity/Results_Uncertainty_95CI.csv')
alpha_df = alpha_df.dropna()
cp_df = pd.read_csv('specific heat/STAResults_Uncertainty_95CI.csv')
# cp_df = cp_df.dropna()


def rho_T(T):
    return 1.6 - 0.000025 * T


def cp_T(T):
    # fit from matlab for cp from 200C to 500C using same form as literature fit
    # a = 1.597
    # b = 0.0002746
    # c = -117.8
    # d = -0.2472
    # e = 0.7528
    # f = 0.276
    T = T+273
    a = 2.126
    b = 0
    c = -481.5
    d = -0.6239
    e = 0.9443
    f = 0.4909
    g = 0.4893
    cp_lit_fit2 = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0)
    return cp_lit_fit2


def cp_lit(T):
    T = T + 273.15
    return (0.538657 + 9.11129e-6*T - 90.2725*T**(-1.0) - 43449.3*T**(-2.0) + 1.59309e7*T**(-3.0) - 1.43688e9*T**(-4.0))*4.184


def alpha_T(T):
    # a = 4.226
    # b = -0.0006108
    # c = 1149
    # d = -8.437e+04
    # e = 2.72e+06
    # f = -3.053e+07
    T = T+273
    a = 3.791
    b = -0.001972
    c = 2363
    d = -1261
    e = 73.38
    f = 0.7805
    g = 0.6753
    h = 0.006715
    k = 9.549e-07

    alpha_fit = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0) + h*T**(-6.0) + k*T**2
    return alpha_fit


T_alpha = alpha_df['Temperature_C']
alpha = alpha_df['AvgThermDiff_mm2_s']
alpha_err = alpha_df['Uncertai95CI_mm2_s']
alpha_fit = np.polyfit(T_alpha, alpha, 5)
fig = plt.figure(num=1, clear=True)
plt.plot(T_alpha, alpha, 'ro', label='Thermal Diffusivity', markerfacecolor='none', markersize=4)
plt.fill_between(T_alpha, alpha-alpha_err, alpha+alpha_err, color='r', alpha=0.25)
# plt.plot(T_alpha, np.polyval(alpha_fit, T_alpha), label='Thermal Diffusivity Fit')
plt.plot(T_alpha, alpha_T(T_alpha), 'b', label='Thermal Diffusivity Fit', zorder=10)
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Diffusivity (mm$^2$/s)')
plt.legend()
# plt.grid()
plt.tight_layout()
T_cp = cp_df['Temperature_C']
cp = cp_df['AvgSpeciHeat_J_gK']
cp_err = cp_df['Uncertai95CI_J_gK']
cp_min = cp - cp_err
cp_max = cp + cp_err
plt.savefig('alpha_fit.pdf')

# T = T_alpha + 273.15
# T = 300
# cp_lit = (0.630375 - 1.60535e-5*T - 225.861 *
#           T**(-1.0) + 3100.1*T**(-2.0) - 910737*T**(-3.0) - 9.64607e7*T**(-4.0))*4.184

T_cp_fit = np.linspace(200, 2500, 100)
T_k = np.linspace(25, 2000, 1000)
fig = plt.figure(num=2, clear=True)
plt.plot(T_cp[:26], cp[:26], 'ro', markerfacecolor='none', label='Specific Heat Average', markersize=4)
plt.errorbar(T_cp[:26], cp[:26], yerr=cp_err[:26], color='r', capsize=2)
# plt.plot(T_k, np.polyval(cp_fit, T_k), 'b', label='Specific Heat Fit')
plt.plot(T_cp_fit, cp_lit(T_cp_fit), 'k--', label='Specific Heat Literature')
plt.plot(T_cp_fit, cp_T(T_cp_fit), 'b', label='Specific Heat Fit', zorder=10)
# plt.plot(T_alpha, np.polyval(cp_fit_lit, T_alpha), '--', label='Specific Heat Literature Fit')
plt.legend()
# plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Specific Heat (J/gK)')
plt.tight_layout()

plt.savefig('cp_fit.pdf')

fig = plt.figure(num=4, clear=True)
plt.plot(T_k, rho_T(T_k), 'b', label='Density')
plt.xlabel('Temperature (C)')
plt.ylabel('Density (g/cm$^3$)')
# plt.grid()
plt.savefig('rho_fit.png')

# cp_df = cp_df[:-4]
cp_df = cp_df.fillna(0)
k = cp_T(cp_df['Temperature_C']) * cp_df['AvgThermDiff_mm2_s'] * rho_T(cp_df['Temperature_C'])
k_err = cp_df['Uncertai95CI_mm2_s'] + cp_df['Uncertai95CI_J_gK']
cp_df['k'] = k
cp_df.to_csv('k_results.csv', index=False)
k_fit = rho_T(T_k) * cp_T(T_k) * alpha_T(T_k)
fig = plt.figure(num=3, clear=True)
plt.plot(cp_df['Temperature_C'], k, 'ro', label='Measured Data', markerfacecolor='none', markersize=4)
plt.fill_between(cp_df['Temperature_C'], k-k_err, k+k_err, color='r', alpha=0.25)
# plt.errorbar(cp_df['Temperature_C'], k, yerr=k_err, color='r', capsize=2)
plt.plot(T_k, k_fit, 'b', label='Fit and Extrapolation', zorder=10)
# plt.grid()
plt.legend()
plt.xlabel('Temperature (C)')
plt.ylabel('Thermal Conductivity (W/mK)')
plt.tight_layout()
plt.savefig('k_fit.pdf')


plt.show()
