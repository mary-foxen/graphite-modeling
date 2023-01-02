def cp_graphite(T):
    # fit from matlab for cp from 200C to 500C using same form as literature fit
    T = T+273
    a = 2.208
    b = 1.838e-07
    c = -508.9
    d = -2.476
    e = 0.8138
    f = 0.6935
    g = 0.3171
    cp_lit_fit2 = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0)
    return cp_lit_fit2


def rho_graphite(T):
    return 1.56 - 0.000025 * T


def cp_putty(T):
    T = T + 273.15
    return (0.538657 + 9.11129e-6*T - 90.2725*T**(-1.0) - 43449.3*T**(-2.0) + 1.59309e7*T**(-3.0) - 1.43688e9*T**(-4.0))*4.184*1.5


def rho_putty(T):
    return 1.4 - 0.000025 * T


def k_putty(T):
    a = 1.801
    b = 5.564e-05
    c = -14.43
    d = 20.44
    e = 1.366
    f = 0.9919
    g = 0.5472
    k_fit = a + b*T + c*T**(-1.0) + d*T**(-2.0) + e*T**(-3.0) + f*T**(-4.0) + g*T**(-5.0)
    return k_fit


T = 200
print(cp_graphite(T), rho_graphite(T), cp_putty(T), rho_putty(T), k_putty(T))
