import pandas as pd
import numpy as np
from math import *

def trinomial(s, x, T, r, sigma, n, Type):
    deltaT = T/n
    u = exp(sigma*sqrt(2*deltaT))
    d = 1.0/u
    pu = pow((exp(r*deltaT/2)-exp(-sigma*sqrt(deltaT/2)))/(exp(sigma*sqrt(deltaT/2))-exp(-sigma*sqrt(deltaT/2))),2)
    pd = pow((exp(sigma*sqrt(deltaT/2))-exp(r*deltaT/2))/(exp(sigma*sqrt(deltaT/2))-exp(-sigma*sqrt(deltaT/2))),2)
    pm = 1-pu-pd
    v = [[0 for j in range(2*i+1)] for i in range(n+1)]
    if Type == 'call':
        for j in range(0, 2*n+1):
             #Calculate the payoff of Call option at the bottom of the trinnomial tree
            v[n][j] = max(s * u**n * d**j - x, 0.0)
    else:
        for j in range(0, 2*n+1):
             #Calculate the payoff of Put option at the bottom of the binnomial tree
            v[n][j] = max(x - s * u**n * d**j, 0.0)
    for i in range(n-1, -1 , -1):
        for j in range(0,2*i+1):
            #Calculate backward the option price
            v[i][j] = exp(-r*deltaT)*(pu*v[i+1][j]+pm*v[i+1][j+1]+pd*v[i+1][j+2])
    return v[0][0]

S = 100
sigma = 0.1
strike = 100
T = 1
r = 0.05
n = 100
Call = 'call'
Put = 'put'
Callprice = trinomial(S,strike,T,r,sigma,n,Call)
Putprice = trinomial(S,strike,T,r,sigma,n,Put)
print("The price of European Call is", Callprice)
print("The price of European Put is", Putprice)