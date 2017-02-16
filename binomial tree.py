import pandas as pd
import numpy as np
from math import *

def binomialEur(s, x, T, r, sigma, n, Type):
    deltaT = T/n
    u = exp(sigma*sqrt(deltaT))
    d = 1.0/u
    a = exp(r*deltaT)
    p = (a-d)/(u-d)
    v = [[0 for j in range(i+1)] for i in range(n+1)]
    if Type == 'call':
        for j in range(0, n+1):
            #Calculate the payoff of Call option at the bottom of the binnomial tree
            v[n][j] = max(s * u**j * d**(n-j) - x, 0.0)    
    else:
        for j in range(0, n+1):
            #Calculate the payoff of Put option at the bottom of the binnomial tree
            v[n][j] = max(x - s * u**j * d**(n-j), 0.0)    
    for i in range(n-1, -1 , -1):
        for j in range(0,i+1):
            #Calculate backward the option price
            v[i][j] = exp(-r*deltaT)*(p*v[i+1][j+1]+(1.0-p)*v[i+1][j])
    return v[0][0]

def binomialAme(s, x, T, r, sigma, n, Type):
    deltaT = T/n
    u = exp(sigma*sqrt(deltaT))
    d = 1.0/u
    a = exp(r*deltaT)
    p = (a-d)/(u-d)
    v = [[0 for j in range(i+1)] for i in range(n+1)]
    if Type == 'call':
        for j in range(0, n+1):
            #Calculate the payoff of Call option at the bottom of the binnomial tree
            v[n][j] = max(s * u**j * d**(n-j) - x, 0.0)
    else:
        for j in range(0, n+1):
            #Calculate the payoff of Put option at the bottom of the binnomial tree
            v[n][j] = max(x - s * u**j * d**(n-j), 0.0)
    for i in range(n-1, -1 , -1):
        for j in range(0,i+1):
            if Type == 'call':
                #Calculate backward the option price and compare the benefit of exercising the Call option with holding
                v[i][j] = max(exp(-r*deltaT)*(p*v[i+1][j+1]+(1.0-p)*v[i+1][j]), s * u**j * d**(i-j)-x)
            else:
                #Calculate backward the option price and compare the benefit of exercising the Put option with holding
                v[i][j] = max(exp(-r*deltaT)*(p*v[i+1][j+1]+(1.0-p)*v[i+1][j]), x-s * u**j * d**(i-j))
    return v[0][0]

S = 100
sigma = 0.1
strike = 100
T = 1
r = 0.05
n = 100
Call = 'call'
Put = 'put'
CallofEur = binomialEur(S,strike,T,r,sigma,n,Call)
PutofEur = binomialEur(S,strike,T,r,sigma,n,Put)
CallofAme = binomialAme(S,strike,T,r,sigma,n,Call)
PutofAme = binomialAme(S,strike,T,r,sigma,n,Put)
print ("The price of European Cal is", CallofEur)
print ("The price of European Put is", PutofEur)
print ("The price of American Cal is", CallofAme)
print ("The price of American Put is", PutofAme)