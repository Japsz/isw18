library(gdata)

setwd("C:/Users/elcro/Documents/GitHub/isw18/R")

#Data -> Date,Open,High,Low,Close,Adj Close,Volume
data = read.csv("GOOGL.csv")

#Simula el comportamiento de una accion, gracias al vector que se ingrese en remaining
simulate <- function(value, dt, r, sigma, remaining) {
	if(length(remaining) == 0){
		return(value)
	}
	eps <- remaining[1]
	remaining <- remaining[-1]
	value <- value + (r*value*dt) + (value*sigma*eps*sqrt(dt))
	return(simulate(value, dt, r, sigma, remaining))
}

#Calcula el sigma de un conjunto de acciones.
get_sigma <- function(list){
	rlist = c()
	for(i in 2:length(list)){
		rlist = c(rlist,log(list[i]/list[i-1]))
	}
	return(sd(rlist))
}


get_buyop <- function(sval, T_num, n_intrv, r, sd, val_inf){
	tot = 0.0
	s_T = 0.0
	for(i in 1:100){
		var = simulate(sval, T_num/n_intrv, r*T_num, sd, rnorm(1000))
		tot = tot + max(c(0,var-val_inf))
		s_T = s_T + var
	}
	tot = tot/5000
	s_T = s_T/5000
	return(exp(-1*r*T_num)*tot)
}


#MAIN
n_intrv = 512 
T_num = length(data$Close)/365.0
sd = get_sigma(data$Close)
opc_value = get_buyop(data$Close[length(data$Close)], T_num, n_intrv, 0.026, sd, data$Close[length(data$Close)])
print(opc_value)