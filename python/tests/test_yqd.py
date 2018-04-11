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

def simular(valor,deltat,r,sigma,restantes):
    if len(restantes) == 0:
        return valor
    eps, restantes = restantes[0],restantes[1:]
    valor = valor + r*valor*deltat + valor*sigma*eps*np.sqrt(deltat)
    return simular(valor,deltat,r,sigma,restantes)

def get_rsigma(list):
    rlist = []
    for i in range(1,len(list)):
        rlist.append(np.log(list[i]/list[i-1]))
    return np.std(np.array(rlist))

def get_opc_compra(sval,T_num,n_intrv,r,sd,val_inf):
    tot = 0
    s_T = 0
    for i in range(0,10000):
        var = simular(sval,T_num/n_intrv,r*T_num,sd,np.random.normal(0,1,n_intrv))
        tot += np.amax([0,var-val_inf])
        s_T += var
    tot = tot/10000
    s_T = s_T/10000
    print("s_T@@var")
    print(s_T)
    return ((np.e)**(-1*r*T_num))*tot


def test(ticker,desde,hasta):
    # Download quote for stocks
    clarray = []
    for string in load_quote(ticker,desde,hasta):
        print(string)
        array = string.split(",")
        clarray.append(float(array[4]))
    sd = get_rsigma(clarray)
    print("sd@@sd")
    print(sd)
    n_intrv = 100 # la simulación tendra "n_intrv" pasos
    T_num = float(len(clarray)/365)
    opc_value = get_opc_compra(clarray[-1],T_num,n_intrv,0.0206,sd,clarray[-1]-10)
    print("opc@@opc")
    print(opc_value)


if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])
