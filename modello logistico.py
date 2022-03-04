import numpy as np
import matplotlib.pyplot as plt

r = 0.5
k = 20

def f(x):
    '''equazione da risolvere
    '''
    x_dot = x*r*(1 - x/k)
    return x_dot


dt = 0.001
num_steps = 20000

def RK4(x0):
    '''risoluzione tramite runge-kutta di ordine 4
    '''
    x = np.zeros(num_steps + 1)
    t = np.zeros(num_steps + 1)

    x[0] = x0

    for i in range(num_steps):
        xk1 = f(x[i])
        xk2 = f(x[i] + xk1*dt/2)
        xk3 = f(x[i] + xk2*dt/2)
        xk4 = f(x[i] + xk3*dt)
        x[i + 1] = x[i] + (dt/6)*(xk1 + 2*xk2 + 2*xk3 + xk4)
        t[i + 1] = t[i] + dt

    return x, t

plt.figure(1)
plt.suptitle('Modello logistico', fontsize=15)
plt.title('Indipendenza del flesso dalle condizioni iniziali', fontsize=15)
for i in np.arange(0.1, 1.1, 0.1):
    x, t = RK4(i)
    plt.plot(t, x, 'blue')

plt.plot(t, (k/2)*np.ones(len(t)), linestyle='--', color='k')
plt.xlabel('Tempo')
plt.ylabel('Popolazione')
plt.grid()

##Mappa logistica

def lm(y, r):
    '''equazione logistica
    '''
    return y*r*(1 - y)

P = []
R = []

def sum(y0, r):
    '''calcolo della popolazione
    '''
    n = y0
    for i in range(1, 400):
        n = lm(n, r)
    P.append(n)
    R.append(r)

for k in np.arange(0.05, 0.95, 0.01):
    for i in np.arange(2., 4.01, 0.01):
        sum(k, i)

plt.figure(2)
plt.title('Diagramma delle biforcazioni mappa logistica', fontsize=15)
plt.plot(R, P, linestyle='', marker='.')
plt.xlabel('r')
plt.ylabel('$x_n$')
plt.grid()

plt.show()