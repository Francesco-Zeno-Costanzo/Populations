# Populations
simple codes of population dynamics

The SIR.py code solves the SIR model with RK4 showing how the maximum number of infected is linked to the number of susceptible to the ratio of the healing and counting coefficients of the model

The code "logistic model.py" shows the growth of a population according to the same model and shows the bifurcation diagram

The Lotka-Volterra.py code solves the equations of the same name in the case of a predatory prey relationship

The Game_of_life.py code returns an animation of the game by putting together various plots of each generation, starting from a generation zero extracted at random or starting from an existing one that can be created using the Gol_gen_0.py code

At each step in time, the following transitions occur:

Any live cell with fewer than two live neighbours dies, as if by underpopulation;

Any live cell with two or three live neighbours lives on to the next generation;

Any live cell with more than three live neighbours dies, as if by overpopulation;

Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The virus.py code simulates the spread of a virus. The population is represented by balls that bounce inside a box, colliding elastically and depending on certain parameters, they become infected and heal. The population is divided into three categories as in the SIR model. The animation can be shown directly at the end of execution (but has problems in saving), or built as for Game_of_life, that is, by combining various graphics

![](epi.gif)  
![](life.gif)
