import sys
import numpy as np
import yqd

def load_quote(ticker,desde,hasta):
	return yqd.load_yahoo_quote(ticker, desde, hasta)[1:-1]

def get_rsigma(list):
    rlist = []
    for i in range(1,len(list)):
        rlist.append(np.log(list[i]/list[i-1]))
    return np.std(np.array(rlist))

def test(ticker,desde,hasta):
    # Download quote for stocks
    clarray = []
    for string in load_quote(ticker,desde,hasta): #parseo
        print(string)
        array = string.split(",")
        clarray.append(float(array[4]))
    sd = get_rsigma(clarray)
    print("sd@@sd") #intercambio con node
    print(sd)
    print("s_T@@sd") #intercambio con node
    print(clarray[-1])

if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])