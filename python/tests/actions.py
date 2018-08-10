import sys
import scipy
import numpy as np
from yahoo_quote_download import yqd

def load_quote(ticker,desde,hasta):
	return yqd.load_yahoo_quote(ticker, desde, hasta)[1:-1]

def test(ticker,desde,hasta):
    # Download quote for stocks
    filename = "{0}{1}{2}.csv".format(ticker,desde,hasta)
    file = open("./files/"+filename,'w')
    file.write('Date,Open,High,Low,Close,Adj Close,Volume\n')
    print(filename)
    for string in load_quote(ticker,desde,hasta): #parseo
        print(string)
        file.write(string+"\n")
    file.close()
    return

if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])