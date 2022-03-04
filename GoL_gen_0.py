import numpy as np
from matplotlib import pyplot as plt

print('Se il file non esiste, viene creato ad programma\nil file deve essere txt')
p = input('inserire path dove salvare al configurazione inizale:\n')

path = r'%s.txt'%p
n = int(input('Numero righe:'))
m = int(input('Numero colonne:'))

fig = plt.figure(1)
plt.title('Generazione zero del gioco')
a = np.zeros((n, m), dtype='i')
plt.pcolor(a)
plt.xticks(range(m))
plt.yticks(range(n))
plt.grid(color='yellow')

def onclick(event):
    x=event.xdata
    y=event.ydata
    a.T[int(x), int(y)] = 1 #la cella selezionoata diventa viva
    plt.pcolor(a)
    plt.grid(color='yellow')
    plt.draw()

    #la matrice viene ogni volta sovrascitta sul file
    #che verra poi letto dal codice Game_of_life
    file = open(path, "w")

    for i in range(n):
        for j in range(m):
            file.write(str(a[i, j]))
            file.write('\t')

        file.write('\n')

    file.close()

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()