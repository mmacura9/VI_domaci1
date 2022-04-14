# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:19:50 2022

@author: mm180261d
"""

import numpy as np
import random
import math

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

def sk(x: np.array, T: np.array, Mk: int) -> np.array:
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
    Resenje jednacine.

    """
    output = x
    k = 0
    while T[k]!=0:
        for m in range(Mk):
            razlika = (T[k]*(np.random.rand(1, 3)[0] - 0.5))
            x1 = x + razlika - razlika.astype(int)
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
        k = k+1
    return output

if __name__ == "__main__":
    T = np.arange(21)/10
    T = np.flip(T)
    x = np.random.rand(1, 3)*2
    x = x[0]
    x = sk(x, T, 10)