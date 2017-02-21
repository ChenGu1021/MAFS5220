import scipy as sp
from scipy.stats import norm
from math import *

def bs_call(S, X, T, r, sigma):
    d1 = (log(S/X)+(r+sigma*sigma/2)*T)/(sigma*sqrt(T))   
    d2 = d1-sigma*sqrt(T)
    callprice = S*norm.cdf(d1)-X*exp(-r*T)*norm.cdf(d2)     #Calculate the Call price
    delta = norm.cdf(d1)                                    #Calculate the delta value
    return {'delta':delta, 'callprice':callprice}

def delta_hedge(S, sigma, strike, T, r, mu, n_steps):
    cash = 0.0
    dt = T/n_steps
    #sp.random.seed(12345)
    delta = 0.0
    call = bs_call(S,strike,T,r,sigma)
    cash -= call['callprice']                               #Firstly, buy a Call option
    x = range(0, int(n_steps), 1)
    for i in x:
        call = bs_call(S,strike,T,r,sigma)
        #Calculate the amount of stock to delta hedge and positive means buying stocks while negative has the contrary meaning
        BuyorSell = -call['delta'] + delta                  
        cash -= BuyorSell*S
        delta = call['delta']
        print ( "Day", i+1, "Stock price:", S, "Delta:", delta)
        print ("Amount  for buying/selling" , BuyorSell)
        e = sp.random.normal(0,1)
        #Simulate the next day's stock price by the Geometric Brownian motion
        S = S*exp((mu-0.5*pow(sigma,2))*dt+sigma*sqrt(dt)*e)
        T -= dt
        cash *= exp(r*dt)            #The cash gets interests at the end of the day
    #On the maturity, the cash won't get the interests so that we require to get rid of this part
    cash /= exp(r*dt)                       
    return cash+max(0,S-strike)-delta*S       #Return the total P&L of the whole duration
S = 100
sigma = 0.1
strike = 100
T = 1.0
r = 0.05
mu = 0.1
n_steps = 365 
PNL = delta_hedge(S,sigma,strike,T,r,mu,n_steps)
print ("The total P&L in one year is ", PNL)
