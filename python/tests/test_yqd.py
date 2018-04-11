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

def simular(valor,deltat,r,sigma,restantes): # Hace una simulación recursiva hasta el último valor t (no quedan números aleatorios)
# inputs:  simular(
# valor: valor a proyectar hacia el futuro,
# deltat: tiempo de proyección,
# r: risk free rate reducido con respecto a Tmayús,
# sigma: desviación estandar r_j
# restantes: lista con valores aleatorios de una distribución normal
#)
    if len(restantes) == 0:
        return valor
    eps, restantes = restantes[0],restantes[1:] # consigue el primer valor y los saca de la siguiente iteración
    valor = valor + r*valor*deltat + valor*sigma*eps*np.sqrt(deltat) #Cálculo siguiente valor
    return simular(valor,deltat,r,sigma,restantes) #siguiente iteración

def get_rsigma(list): #consigue la desviación estandar de los r_j para una lista de valores de clausura
    rlist = []
    for i in range(1,len(list)):
        rlist.append(np.log(list[i]/list[i-1]))
    return np.std(np.array(rlist))

def get_opc_compra(sval,T_num,n_intrv,r,sd,val_inf): #Consigue el valor de una opcion
# inputs: get_opc_compra(
# sval: valor inicial de cada simulación,
# T_num: Tmayús como número con respecto a 1 año = 1,
# n_intrv: número de intervalos a dividir el tiempo Tmayús(N°iteraciones x simulación),
# r: risk free rate anual,
# sd: desviación estandar r_j
# val_inf: valor de inferencia (exprimentación)
#)
    tot = 0
    s_T = 0
    for i in range(0,5000): #iteracion para hacer 5000 simulaciones
        var = simular(sval,T_num/n_intrv,r*T_num,sd,np.random.normal(0,1,n_intrv)) #entrega el último valor observado tras la simulación
        tot += np.amax([0,var-val_inf]) # para obtener esperanza de fi
        s_T += var # para obtener valor final promedio de la simulación
    tot = tot/5000 #esperanza fi
    s_T = s_T/5000 #vfprom
    print("s_T@@var")#intercambio con node
    print(s_T)
    return ((np.e)**(-1*r*T_num))*tot #retorna F(val_inf,0)


def test(ticker,desde,hasta):
    # Download quote for stocks
    clarray = []
    for string in load_quote(ticker,desde,hasta): #parseo
        print(string)
        array = string.split(",")
        clarray.append(float(array[4]))
    sd = get_rsigma(clarray) # se consigue sigma
    print("sd@@sd") #intercambio con node
    print(sd)
    n_intrv = 512 # la simulación tendra "n_intrv" pasos
    T_num = float(len(clarray)/365) # valor Tmayús con respecto 1 = 1 año
    opc_value = get_opc_compra(clarray[-1],T_num,n_intrv,0.0206,sd,clarray[-1])# se avalúa siendo usando el último valor histórico como valor de inferencia/experimentación
    print("opc@@opc") #intercambio con node
    print(opc_value)


if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])
