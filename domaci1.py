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

def ga(num: int, iteracije: int) -> tuple:
    """
    
    
     Parameters
    ----------
    num : int
        Velicina populacije.
    iteracije : int
        Broj iteracija.

    Returns
    -------
    tuple
        Genetski algoritam.

    """
    # inicijalizacija
    x = np.random.rand(num, 3)*2
    verovatnoce = np.arange(num) + 1
    verovatnoce = verovatnoce / np.sum(verovatnoce)
    verovatnoce = np.flip(verovatnoce)
    verovatnoce = np.cumsum(verovatnoce)
    prosecni = []
    najbolji = []
    for k in range(iteracije):
        suma = 0
        for i in x:
            suma = suma + func(i)
        prosecni = prosecni + [suma/num]
        naj_deca = list(x)
        naj_deca = sorted(naj_deca, key=func)
        najbolji = najbolji + [func(naj_deca[0])]
        za_ukrstanje = np.random.rand(1, int(1.8*num))[0]
        # selekcija
        for i in range(int(1.8*num)):
            for j in range(int(1.8*num)):
                if za_ukrstanje[i] < verovatnoce[j]:
                    za_ukrstanje[i] = j
                    break
        
        x = np.array([])
        for i in range(int(1.8*num)//2):
            # ukrstanje
            prvi = naj_deca[int(za_ukrstanje[2*i])]
            drugi = naj_deca[int(za_ukrstanje[2*i+1])]
            novi = np.zeros(3)
            presek = random.randint(1, 2)
            if presek == 1:
                novi[0] = math.sqrt(prvi[0]*drugi[0])
                novi[1] = math.sqrt(prvi[1]*drugi[2])
                novi[2] = math.sqrt(prvi[2]*drugi[1])
            else:
                novi[0] = math.sqrt(prvi[0]*drugi[1])
                novi[1] = math.sqrt(prvi[1]*drugi[0])
                novi[2] = math.sqrt(prvi[2]*drugi[2])
            # mutacija
            verovatnoca_mutacije = np.random.rand(1,3)[0]
            mutacija = np.random.rand(1, 3)[0]*0.2 - 0.1
            mutacija[verovatnoca_mutacije>0.2] = 0
            novi = novi + mutacija
            novi[novi<0] = 0
            novi[novi>2] = 2
            if x.size == 0:
                x = novi
            else:
                x = np.vstack([x, novi])
        for i in range(num//10):
            x = np.vstack([x, naj_deca[i]])
    naj_deca = list(x)
    naj_deca = sorted(naj_deca, key=func)
    suma = 0
    for i in x:
        suma = suma + func(i)
    prosecni = prosecni + [suma/num]
    najbolji = najbolji + [func(naj_deca[0])]
    return np.array(prosecni), np.array(najbolji)

if __name__ == "__main__":
    prosecni = np.array([])
    najbolji = np.array([])
    
    for i in range(100):
        p, n = ga(20, 15)
        if prosecni.size == 0:
            prosecni = p
            najbolji = n
        else:
            prosecni = prosecni + p
            najbolji = najbolji + n
            
    prosecni = prosecni/100
    najbolji = najbolji/100
    t1 = np.arange(najbolji.size)*20
    plt.plot(t1, prosecni, t1, najbolji)
    plt.title('genetski algoritam sa parametrima 20, 15')
    plt.legend(['prosecno resenje', 'najbolje resenje'])
    plt.ylim(0, 3)
    plt.xlabel('iteracije')
    plt.ylabel('izlaz funkcije')