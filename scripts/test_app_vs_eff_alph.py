import numpy as np

L = 4e-3  # m
L_g = 2e-3  # m
L_p = 2e-3  # m
alpha_g = 4.16e-6  # m^2/s
alpha_p = 0.714e-6  # m^2/s
k_g = 10  # W/mK
k_p = 2  # W/mK
lambda_g = k_g/np.sqrt(alpha_g)
lambda_p = k_p/np.sqrt(alpha_p)
lambda_gp = lambda_g/lambda_p
K = lambda_gp/(lambda_gp+1)
A_F = 0.5 - 0.3592*(K - 0.5)
A_S = 0.3572*(K - 0.5)**2
eta_g = L_g**2/alpha_g
eta_p = L_p**2/alpha_p
eta_gp = eta_g/eta_p
eta_pg = eta_p/eta_g
eta_e = 2*eta_g*((A_F - 2*A_S) + (1-A_F+A_S)*eta_pg + A_S*eta_gp)
alpha_e = L**2/eta_e
print(alpha_e)
