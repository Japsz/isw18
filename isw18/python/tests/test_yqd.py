# -*- coding: utf-8 -*-
"""
Created on Sat May 20 18:58:59 2017

@author: c0redumb
"""
import sys
import numpy as np

# Hace una simulación recursiva hasta el último valor t (no quedan números aleatorios)
# inputs:  simular(
# valor: valor a proyectar hacia el futuro,
# deltat: tiempo de proyección,
# r: risk free rate reducido con respecto a Tmayús,
# sigma: desviación estandar r_j
# restantes: lista con valores aleatorios de una distribución normal
#)
def simular(valor,deltat,r,sigma,restantes):
    if len(restantes) == 0:
        return valor
    eps, restantes = restantes[0],restantes[1:] # consigue el primer valor y los saca de la siguiente iteración
    valor = valor + r*valor*deltat + valor*sigma*eps*np.sqrt(deltat) #Cálculo siguiente valor
    print(valor)
    return simular(valor,deltat,r,sigma,restantes) #siguiente iteración

#consigue la desviación estandar de los r_j para una lista de valores de clausura
def get_rsigma(list):
    rlist = []
    for i in range(1,len(list)):
        rlist.append(np.log(list[i]/list[i-1]))
    return np.std(np.array(rlist))

#Consigue el valor de una opcion
# inputs: get_opc_compra(
# sval: valor inicial de cada simulación,
# T_num: Tmayús como número con respecto a 1 año = 1,
# n_intrv: número de intervalos a dividir el tiempo Tmayús(N°iteraciones x simulación),
# r: risk free rate anual,
# sd: desviación estandar r_j
# val_inf: valor de inferencia (exprimentación)
#)
def get_opc_compra(sval,T_num,n_intrv,r,sd,val_inf,n_sims):
    tot_c = 0
    tot_v = 0
    s_T = 0
    print("sims@@sims")
    for i in range(0,n_sims): #iteracion para hacer 5000 simulaciones
        var = simular(sval,T_num/n_intrv,r*T_num,sd,np.random.normal(0,1,n_intrv)) #entrega el último valor observado tras la simulación
        tot_c += np.amax([0,var - val_inf]) # para obtener esperanza de fi
        tot_v += np.amax([0,val_inf - var]) # para obtener esperanza de fi
        s_T += var # para obtener valor final promedio de la simulación
        print("simfin@@fin")
    tot_c = tot_c/n_sims #esperanza fi
    tot_v = tot_v/n_sims #esperanza fi
    s_T = s_T/n_sims #vfprom
    print("s_T@@var")#intercambio con node
    print(s_T)
    return (((np.e)**(-1*r*T_num))*tot_c,((np.e)**(-1*r*T_num))*tot_v) #retorna F(val_inf,0)


def test(r,ej_price,T_num,n_sims,n_intrv,s_val,sd):
    # la simulación tendra "n_intrv" pasos
    # valor Tmayús con respecto 1 = 1 año
    opc_value_c,opc_value_v = get_opc_compra(float(s_val),float(T_num),int(n_intrv),float(r),float(sd),float(ej_price),int(n_sims))# se avalúa siendo usando el último valor histórico como valor de inferencia/experimentación
    print("opc@@opc") #intercambio con node
    print(opc_value_c)
    print("opv@@opc") #intercambio con node
    print(opc_value_v)


if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])

