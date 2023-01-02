import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp

plt.style.use(['science', 'grid'])
x = np.linspace(0.01,10,100)
# y = 1+2*(-1/(np.exp(x)+1))
jtheta = np.vectorize(mp.jtheta, 'D')
y = jtheta(4, 0, np.exp(-x))
plt.plot(x,y,'b-')
plt.hlines(0.5,0,10,'k','--')
plt.vlines(1.38, 0, 1, 'k', '--')
plt.xlabel('$\omega = \pi^2 \\alpha t / L^2$')
plt.ylabel('$\Theta = T/T_{max}$')
plt.tight_layout()
plt.savefig('LFA_profile.pdf')
plt.show()