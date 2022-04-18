# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:19:50 2022

@author: mm180261d
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import random

def func(x: np.array) -> float:
    """
    

    Parameters
    ----------
    x : np.array
        Ulaz u funkciju.

    Returns
    -------
    float
        Izlaz funkcije koju treba minimizovati.

    """
    if x.size != 3:
        return 1000000
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    return 4*(x1*x1 + x2*x2 - x1*x2)**(0.75)/3 + x3

def sk(x: np.array, T: np.array, Mk: int) -> tuple:
    """
    

    Parameters
    ----------
    x : np.array
        Pocetno stanje.
    T : np.array
        Raspored temperatura.
    Mk : int
        Broj iteracija za svaku temperaturu.

    Returns
    -------
    Niz najboljih resenja i niz trenutnih resenja.

    """
    output = x
    foutput = []
    fx = []
    k = 0
    while k<=T.size and T[k]!=0:
        for m in range(Mk):
            razlika = (np.random.rand(1, 3)[0]- 0.5)
            x1 = x + razlika
            x1[x1<0] = 0
            x1[x1>2] = 2
            delta = func(x1) - func(x)
            if func(x1) < func(output):
                output = x1
            if delta <= 0:
                x = x1
            else:
                if random.random() <= math.exp(-delta/T[k]):
                    x = x1
            fx = fx + [func(x)]
            foutput = foutput + [func(output)]
        k = k+1
    return output, x, foutput, fx

def pps(bd: int) -> tuple:
    """
    
    
    
     Parameters
    ----------
    bd : int
        Broj dece.

    Returns
    -------
    tuple
        Pretraga po snopu.

    """
    x = np.random.rand(bd, 3)*2
    najbolje = 10000
    najbolje_x = x[0, :]
    najbolje1 = 100000
    while najbolje < najbolje1:
        najbolje1 = najbolje
        lista_najboljih = []
        f_najboljih = []
        for i in x:
            lista_najboljih = lista_najboljih + [i]
            f_najboljih = f_najboljih + [func(i)]
            
        lista_najboljih = [i for _,i in sorted(zip(f_najboljih, lista_najboljih))]
        lista_najboljih = lista_najboljih[0:5]
        x = np.array([])
        for i in lista_najboljih:
            x1 = i + np.random.rand(bd, 3)*0.2-0.1
            x1[x1<0] = 0
            x1[x1>2] = 2
            if x.size == 0:
                x = x1
            else:
                x = np.append(x, x1, axis=0)
            if najbolje > func(i):
                najbolje = func(i)
                najbolje_x = i
    print(najbolje, najbolje_x)

if __name__ == "__main__":
    pps(50)
