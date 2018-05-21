library(gdata)

setwd("C:/Users/elcro/Documents/GitHub/isw18/R")

#Data -> Date,Open,High,Low,Close,Adj Close,Volume
data = read.csv("GOOGL.csv")

#Simulator
simulate <- function(value, dt, r, sigma, remaining) {
	if(length(remaining) == 0){
		return(value)
	}
	eps <- remaining[1]
	remaining <- remaining[-length(remaining)]
	value <- value + (r*value*dt) + (value*sigma*eps*sqrt(dt))
	print(value)
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

get_buyop <- function(){
	
}


#MAIN
n_intrv = 512 

T_num = len(data$Close)/365.0
