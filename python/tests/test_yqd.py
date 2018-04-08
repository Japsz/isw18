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
    if restantes == 0:
        return valor
    valor = r*valor + valor*sigma
    return simular(valor,r,sigma,restantes - 1)

def test(ticker,desde,hasta):
    # Download quote for stocks
    oparray = []
    clarray = []
    for string in load_quote(ticker,desde,hasta):
        print(string)
        array = string.split(",")
        oparray.append(float(array[1]))
        clarray.append(float(array[4]))
    oparray = np.array(oparray)
    print(np.std(oparray))



if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])
