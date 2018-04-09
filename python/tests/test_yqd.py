# -*- coding: utf-8 -*-
"""
Created on Sat May 20 18:58:59 2017

@author: c0redumb
"""
import sys
import sympy as sm
import scipy
import numpy as np

from yahoo_quote_download import yqd

def load_quote(ticker,desde,hasta):
	return yqd.load_yahoo_quote(ticker, desde, hasta)[1:-1]

def simular(valor,r,sigma,restantes):
    if len(restantes) == 0:
        return valor
    eps, restantes = restantes[0],restantes[1:]
    valor = valor + r*valor + valor*sigma*eps
    return simular(valor,r,sigma,restantes)

def test(ticker,desde,hasta):
    # Download quote for stocks
    oparray = []
    clarray = []
    len = 0
    for string in load_quote(ticker,desde,hasta):
        print(string)
        len+=1
        array = string.split(",")
        oparray.append(float(array[1]))
        clarray.append(float(array[4]))
    clarray = np.array(clarray)
    sd = np.std(clarray)
    sd = sd /(len - 1)
    tot = 0
    for i in range(0,10000):
        tot += simular(clarray[-1],0.025,sd,np.random.normal(0,1,len-1))
    tot = tot/10000
    print(tot)


if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])
