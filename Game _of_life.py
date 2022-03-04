import glob
import numpy as np
import random as rn
import imageio as io
from PIL import Image
import matplotlib.pyplot as plt

class GameOfLife:

    def __init__(self, dimx, dimy, gen, k):

        self.dimx = dimx #dimesione griglia su x
        self.dimy = dimy #dimesione griglia su y
        self.gen = gen #numero delle generazioni
        self.old_grid = np.zeros((dimx, dimy), dtype='i')
        self.new_grid = np.zeros((dimx, dimy), dtype='i')
        self.k = k

    def gen_0(self, path=None):
        '''
        Creo lo stato iniziale della griglia se k=0 vi è una
        generazione casuale, se k=1 lo stato inizale viene letto
        da un txt che può essere creato da codice: Gol_gen_0.py
        '''
        if self.k == 0 :
            #condigurazione inizale casuale
            for i in range(self.dimx):
                for j in range(self.dimy):
                    if rn.random() < 0.2:
                        self.old_grid[i][j] = 1 #cella viva
                    else:
                        self.old_grid[i][j] = 0 #cella morta

        if self.k == 1:
            self.old_grid = np.loadtxt(path)

    def vicini(self, i, j):
        '''Calcolo quanti sono i vicini vivi
        '''
        v = 0
        for x in [i-1, i, i+1]:
            for y in [j-1, j, j+1]:
                if x == i and y == j :
                    continue #cella che considero, non devo far nulla
                if x != self.dimx and y != self.dimy :
                    v += self.old_grid[x, y] #conto i vicini

                #condizioni al bordo continue
                elif x == self.dimx and y != self.dimy :
                    v += self.old_grid[0, y]
                elif x != self.dimx and y == self.dimy :
                    v += self.old_grid[x, 0]
                else:
                    v += self.old_grid[0][0]
        return v

    def evoluzione(self):
        '''evoluzione della griglia
        '''
        #salvo la configurazione iniziale per l'animazione
        g = 0
        fig = plt.figure(g)
        plt.title(f"Game of life, generation number = {g}")
        plt.pcolor(self.old_grid)
        plt.savefig(r'C:\Users\franc\Documents\codici python\gif/%d'%(g))
        plt.close(fig)

        while g < self.gen :

            g += 1 #nuova generazione

            for i in range(self.dimx):
                for j in range(self.dimy):
                    n_vivi = self.vicini(i, j)
                    if self.old_grid[i, j] == 1 and n_vivi < 2 :
                        self.new_grid[i, j] = 0 #morte per solitudine
                    if self.old_grid[i, j] == 1 and (n_vivi == 2 or n_vivi == 3) :
                        self.new_grid[i, j] = 1 #continua a vivere
                    if self.old_grid[i, j] == 1 and n_vivi > 3:
                        self.new_grid[i, j] = 0 #morte per sovra-popolazione
                    if self.old_grid[i, j] == 0 and n_vivi == 3 :
                        self.new_grid[i, j] = 1 #nascita nuova cella

            #salvo ogni configurazione per l'animazione
            fig = plt.figure(g)
            plt.title(f"Game of life, generation number = {g}")
            plt.pcolor(self.new_grid)
            plt.savefig(r'C:\Users\franc\Documents\codici python\gif/%d'%(g))
            plt.close(fig)

            #aggiorno la griglia
            self.old_grid = self.new_grid.copy()

def main():

    k = int(input('Digitare 0 per configurazione casuale\nDigitare 1 per inserire configurazione pronta:\n'))
    print("Idipendentemente dall' avere o meno la configurazione iniziale inserire:")
    N = int(input('Numero righe:'))
    M = int(input('Numero colonne:'))
    T = int(input('Per quante generazioni evolvere:'))
    if k == 1:
        p = input('inserire path del file txt con la configurazione inizale:\n')
        path = r'%s.txt'%p
    else:
        path = None

    G = GameOfLife(N, M, T, k)

    G.gen_0(path)

    G.evoluzione()

    frames=[]
    imgs=sorted(glob.glob(r'C:\Users\franc\Documents\codici python\gif/*.png'))
    imgs.sort(key=len)
    for i in imgs:
        new_frame=Image.open(i)
        frames.append(new_frame)

    frames[0].save('life1.gif',format='GIF',append_images=frames[:],save_all=True,duration=100,loop=0)


main()