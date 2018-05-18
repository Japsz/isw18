import sys
import scipy
import numpy as np
from yahoo_quote_download import yqd

def load_quote(ticker,desde,hasta):
	return yqd.load_yahoo_quote(ticker, desde, hasta)[1:-1]

def test(ticker,desde,hasta):
    # Download quote for stocks
    for string in load_quote(ticker,desde,hasta): #parseo
        print(string)

if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])