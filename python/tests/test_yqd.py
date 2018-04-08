# -*- coding: utf-8 -*-
"""
Created on Sat May 20 18:58:59 2017

@author: c0redumb
"""
import sys
import sympy as sm
import scipy
import numpy

from yahoo_quote_download import yqd

def load_quote(ticker,desde,hasta):
	return yqd.load_yahoo_quote(ticker, desde, hasta)[1:-1]

def test(ticker,desde,hasta):
	# Download quote for stocks
	for string in load_quote(ticker,desde,hasta):
	    print(string)
	    array = string.split(",")



if __name__ == '__main__':
	test(sys.argv[1],sys.argv[2],sys.argv[3])