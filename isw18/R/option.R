

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
#No utilizado, se calcula sigma con Python
get_sigma <- function(list){
	rlist = c()
	for(i in 2:length(list)){
		rlist = c(rlist,log(list[i]/list[i-1]))
	}
	return(sd(rlist))
}


get_buyop <- function(s_val, ej_price, T_num, n_sims, n_intrv, r, sd){
	simvalu = c()
	total = 0.0
	s_T = 0.0
	for(i in 1:n_sims){
		var = simulate(s_val, T_num/n_intrv, r*T_num, sd, rnorm(n_intrv))
		simvalu = c(simvalu,var)
		total = total + max(c(0,var - ej_price))
		s_T = s_T + var
	}
	total = total/n_sims
	s_T = s_T/n_sims	
	#plot(simvalu,type="l")
	opt_value = exp(-1*r*T_num)*total
	return(opt_value)
}


#call('R route', {key: args})
#MAIN
main <- function(){
	#Librerias
	if(!library('gdata', logical.return = TRUE)){
		install.packages('gdata')
		library('gdata')
	}
	if(!library('rjson', logical.return = TRUE)){
		install.packages('rjson')
		library('rjson')
	}
	#r, ej_price, T_num, n_sims, n_intrv, s_val, sd

	#Obtenemos parametros desde js
	args <- commandArgs(trailingOnly = TRUE)
	json <- fromJSON(args)
	#json = {key: args}
	#s_val, T_num, n_intrv, r, sd, val_inf, n_sims)
	s_val = as.numeric(json$s_val)
	T_num = as.numeric(json$T_num)
	n_intrv = as.numeric(json$n_intrv)
	r = as.numeric(json$r)
	sd = as.numeric(json$sd)
	val_inf = as.numeric(json$val_inf)
	n_sims = as.numeric(json$n_sims)

	opc_value = get_buyop(s_val,ej_price,T_num,n_sims,n_intrv,r,sd)
	print(toJSON(opc_value))
	return()
}

main()