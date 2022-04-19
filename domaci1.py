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

def pps(bd: int, naj: int) -> tuple:
    """
    
    
    
     Parameters
    ----------
    bd : int
        Broj dece.
    naj : int
        Biranje naj najboljih.

    Returns
    -------
    tuple
        Pretraga po snopu.

    """
    x = np.random.rand(50, 3)*2
    najbolje = 10000
    najbolje_x = x[bd, :]
    najbolje1 = 100000
    prosecni = []
    lista_najboljih = []
    while najbolje < najbolje1:
        najbolje1 = najbolje
        naj_deca = list(x)
        naj_deca = sorted(naj_deca, key=func)
        p = 0
        for i in naj_deca:
            p = p + func(i) 
        naj_deca = naj_deca[0:naj]
        prosecni = prosecni + [p*3/x.size]
        x = np.array([])
        for i in naj_deca:
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
        lista_najboljih = lista_najboljih + [najbolje]
    return lista_najboljih, prosecni

if __name__ == "__main__":
    najbolji = np.array([])
    prosecni = np.array([])
    for i in range(100):
        l_n, pr = pps(3, 2)
        if najbolji.size == 0:
            najbolji = np.array(l_n)
            prosecni = np.array(pr)
        else:
            if najbolji.size < len(l_n):
                while najbolji.size != len(l_n):
                    najbolji = np.append(najbolji, 0)
                    prosecni = np.append(prosecni, 0)
            for j in range(len(l_n)):
                najbolji[j] = najbolji[j]+l_n[j]
                prosecni[j] = prosecni[j]+pr[j]
    najbolji = najbolji/100
    prosecni = prosecni/100
    
    fig, ax = plt.subplots(1, 3, figsize=(20,10), dpi=80);
    t1 = np.arange(najbolji.size)
    ax[0].plot(t1, najbolji, t1, prosecni)
    ax[0].set_title('6 generisanih kandidata')
    ax[0].legend(['prosecno resenje', 'najbolje resenje'])
    ax[0].set_ylim(0, 3)
    ax[0].set_xlabel('iteracije')
    ax[0].set_ylabel('izlaz funkcije')
