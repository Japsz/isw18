library('rjson')
library('gdata')

setwd("Github/isw18/files/")

#Data -> Date,Open,High,Low,Close,Adj Close,Volume

#Se calcula la opcion de compra
get_buyop <- function(sval, T_num, n_intrv, r, sd, val_inf){
	simuls = 200
	simvalu = c()
	total = 0.0
	s_T = 0.0
	for(i in 1:simuls){
		var = simulate(sval, T_num/n_intrv, r*T_num, sd, rnorm(simuls))
		simvalu = c(simvalu,var)
		total = total + max(c(0,var-val_inf))
		s_T = s_T + var
	}
	total = total/simuls
	s_T = s_T/simuls
	return(exp(-1*r*T_num)*total)
}

#Simula el comportamiento de una accion, gracias al vector que se ingrese en remaining
#value: Valor inicial
#dt: intervalos de tiempo
#r: Tasa libre comercio (?)
#sigma: desviacion estandar datos
#remaining: Vector de valores pasados.
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
	for(i in 1:length(list)){
		rlist = c(rlist,log(list[i]/list[i-1]))
	}
	return(sd(rlist))
}



main <- function(filename, r, n_intrv){
	data = read.csv(filename)
	T_num = length(data$Close)/365.0
	sd = get_sigma(data$Close)
	opc_value = get_buyop(data$Close[length(data$Close)], 
					T_num, n_intrv, r, sd, 
					data$Close[length(data$Close)])
	return(opc_value)
}

# get arguments of command line Callsync(rscript,args.)
args <- commandArgs(trailingOnly = TRUE)
# arguments to JSON
json <- fromJSON(args)
# call function
ret <- main(args$a, 0.026, 512)
# convert return of function to list
output <- list(result = ret)
# output JSON
print(toJSON(output));