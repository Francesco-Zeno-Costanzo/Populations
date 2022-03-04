import numpy as np
import random as rn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import glob
import imageio as io
from PIL import Image

suscettibile = 0
infetto = 1
rimosso = 2

class Persona:

    def __init__(self, x, y, vx, vy, state, mal=0, r=0.01):
        self.r = r
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state
        self.mal = mal

    def st(self, state):
        '''
        Modifica lo stato di una persona:
        stato = 0 => persona suscettibile
        stato = 1 => persona infetta
        stato = 2 => persona rimossa
        '''
        self.state = state

    def malattia(self):
        '''aggiorna il contatore che indica la durata della malattia
        '''
        self.mal += 1

    def n_vel(self, vx, vy):
        '''campbio delle velocità
        '''
        self.vx = vx
        self.vy = vy

    def n_pos_m(self, x, y):
        '''cambio delle posizioni
        '''
        self.x = x
        self.y = y

    def n_pos(self, dt):
        '''evoluzione della posizione nel tempo
        '''
        self.x += self.vx*dt
        self.y += self.vy*dt

    def scontro(self, altra):
        '''
        controlla se sue persone si scontrano
        se sì restituisce true
        '''
        dx = self.x - altra.x
        dy = self.y - altra.y
        D = np.sqrt(dx**2 + dy**2)
        if D < self.r + altra.r :
            return True
        else: return False

class Ambiente:

    #limiti della regione
    xr = 1
    xl = 0
    yu = 1
    yd = 0

    #variabili della popolazione
    N_tot = 0
    N_suscettibili = 0
    N_infetti = 0
    N_rimossi = 0

    def __init__(self, persone):
        self.persone = persone

        #valori inizali
        Ambiente.N_tot = len(self.persone)
        for persona in self.persone:
            if persona.state == suscettibile:
                Ambiente.N_suscettibili += 1
            if persona.state == 1:
                Ambiente.N_infetti += 1

    def evolvo(self, dt):
        '''evoluzione del sistema
        '''
        for persona1 in self.persone:
            persona1.n_pos(dt) #aggiorno le posizioni

            #se malato aggiorno il contatore
            if persona1.state == infetto: persona1.malattia()
            for persona2 in self.persone:
                if persona1 != persona2 :

                    #interazione fra le persone, urti elastici fra particelle
                    if persona1.scontro(persona2) :

                        r1 = np.array([persona1.x, persona1.y])
                        r2 = np.array([persona2.x, persona2.y])

                        d = np.linalg.norm(r1 - r2)**2
                        v1 = np.array([persona1.vx, persona1.vy])
                        v2 = np.array([persona2.vx, persona2.vy])

                        u1 = v1 -  np.dot(v1-v2, r1-r2) / d * (r1 - r2)
                        u2 = v2 -  np.dot(v2-v1, r2-r1) / d * (r2 - r1)

                        persona1.n_vel(u1[0], u1[1])
                        persona2.n_vel(u2[0], u2[1])

                        #secondo una certa possibilita la persona si può infettare
                        if persona1.state == infetto:
                            r = rn.uniform(0,1)
                            if r > 0.85 :
                                if persona2.state == suscettibile: #aggiorno variabili della popolazione
                                    if Ambiente.N_infetti <= Ambiente.N_tot - Ambiente.N_suscettibili- Ambiente.N_rimossi :
                                        persona2.st(infetto)
                                        Ambiente.N_infetti += 1
                                        if Ambiente.N_suscettibili > 0:
                                            Ambiente.N_suscettibili -= 1

            #interazione con i muri, utri elastici
            LD = persona1.x + persona1.r >= Ambiente.xr
            LS = persona1.x - persona1.r <= Ambiente.xl
            LU = persona1.y + persona1.r >= Ambiente.yu
            LP = persona1.y - persona1.r <= Ambiente.yd

            if LD or LS :
                persona1.n_vel(-persona1.vx, persona1.vy)
                if LD :
                    persona1.n_pos_m(Ambiente.xr - persona1.r, persona1.y)
                if LS :
                    persona1.n_pos_m(Ambiente.xl + persona1.r, persona1.y)
            if LU or LP :
                persona1.n_vel(persona1.vx, -persona1.vy)
                if LU :
                    persona1.n_pos_m(persona1.x, Ambiente.yu - persona1.r)
                if LP :
                    persona1.n_pos_m(persona1.x, Ambiente.yd + persona1.r)

            #guarigione della persona
            r = rn.uniform(0,1)
            if persona1.mal > 600 and persona1.state == infetto and r > 0.5:
                persona1.st(rimosso)
                 #aggiorno variabili della popolazione
                if Ambiente.N_rimossi <= Ambiente.N_tot - Ambiente.N_suscettibili- Ambiente.N_infetti :
                    Ambiente.N_rimossi += 1
                if Ambiente.N_infetti > 0:
                    Ambiente.N_infetti -= 1

N = 100 #popolazione totale
n = 0
P = []
while n < N: #creo le persone
    if n == N - 1: k = 1
    else : k = 0
    v_x = rn.uniform(-80, 80)
    v_y = rn.uniform(-80, 80)
    x_0 = rn.uniform(0.1, 0.9)
    y_0 = rn.uniform(0.1, 0.9)
    persona = Persona(x_0, y_0, v_x, v_y, k)
    for p in P:
        if p.scontro(persona):
            break #non posso creare due persone nello stesso punto
    else:
        P.append(persona)
        n += 1

dt = 1/10000
T = int(1 / dt)//3
amb = Ambiente(P)

#array che conterrano le informazioni della simulazione
X = np.zeros((2, T, N))
Y = np.zeros((N, T))
S = np.array([])
I = np.array([])
R = np.array([])
p = np.array([])

for t in range(T):
    amb.evolvo(dt)
    for n, persona in enumerate(amb.persone):
        X[:, t, n] = persona.x, persona.y
        Y[n, t] = persona.state
    p = np.insert(p, len(p), t*dt)
    S = np.insert(S, len(S), amb.N_suscettibili)
    I = np.insert(I, len(I), amb.N_infetti)
    R = np.insert(R, len(R), amb.N_rimossi)

SIR = np.array([S, I, R])

##animazione in diretta non salvabile (viena male il grafico delle palline)
fig = plt.figure(1, figsize=(12, 6))
plt.suptitle('Modello epidemico', fontsize=15)
ax1 = fig.add_subplot(121)
ax1.set_xlim(amb.xl, amb.xr)
ax1.set_ylim(amb.yd, amb.yu)

plt.grid()
for s in ['top','bottom','left','right']:
    ax1.spines[s].set_linewidth(2)

ax2 = fig.add_subplot(122)
ax2.set_xlim(0, T*dt)
ax2.set_ylim(-1, N+1)
plt.grid()


def animate(i):
    dot = np.array([])
    Dot = np.array([])

    Dot = np.append(Dot, ax2.plot([], [], 'b-', lw=3))
    Dot = np.append(Dot, ax2.plot([], [], 'r-', lw=3))
    Dot = np.append(Dot, ax2.plot([], [], 'g-', lw=3))
    for k in range(3):
        Dot[k].set_data(p[:i], SIR[k][:i])

    for k in range(N):
        if Y[k, i] == 0:
            dot=np.append(dot, ax1.plot([], [], 'bo'))
        elif Y[k, i] == 1:
            dot=np.append(dot, ax1.plot([], [], 'ro'))
        elif Y[k, i] == 2:
            dot=np.append(dot, ax1.plot([], [], 'go'))
        dot[k].set_data(X[0, i, k], X[1, i, k])

    dot=np.append(dot, Dot)

    return dot

anim = animation.FuncAnimation(fig, animate, frames=range(0, T-1, 6), interval=1, blit=True, repeat=True)

plt.show()

##aniamzione che viene salvata come gif

l = 0
for i in np.arange(0, T-1, 6):

    fig = plt.figure(l, figsize=(12, 6))
    plt.suptitle('Modello epidemico', fontsize=15)
    ax1 = fig.add_subplot(121)
    ax1.set_xlim(amb.xl, amb.xr)
    ax1.set_ylim(amb.yd, amb.yu)

    plt.grid()
    for s in ['top','bottom','left','right']:
        ax1.spines[s].set_linewidth(2)

    ax2 = fig.add_subplot(122)
    ax2.set_xlim(0, T*dt)
    ax2.set_ylim(-1, N+1)
    plt.grid()


    for k in range(N):
        if Y[k, i] == 0:
            ax1.plot(X[0, i, k], X[1, i, k], 'bo')
        elif Y[k, i] == 1:
            ax1.plot(X[0, i, k], X[1, i, k], 'ro')
        elif Y[k, i] == 2:
            ax1.plot(X[0, i, k], X[1, i, k], 'go')

    ax2.plot(p[:i], S[:i], 'b-', lw=3, label='Suscettibili')
    ax2.plot(p[:i], I[:i], 'r-', lw=3, label='Infetti')
    ax2.plot(p[:i], R[:i], 'g-', lw=3, label='Rimossi')
    ax2.legend(loc='best')

    plt.savefig(r'C:\Users\franc\Documents\codici python\gif/%d'%(l))
    plt.close(fig)
    l += 1

frames=[]
imgs=sorted(glob.glob(r'C:\Users\franc\Documents\codici python\gif/*.png'))
imgs.sort(key=len)
for i in imgs:
    new_frame=Image.open(i)
    frames.append(new_frame)


frames[0].save('epi.gif',format='GIF',append_images=frames[:],save_all=True,duration=100,loop=0)
