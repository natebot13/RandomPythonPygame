#!/usr/bin/python

import random
import math

def randomColor(R = None, G = None, B = None, Rmax = 255, Rmin = 0, Bmax = 255, Bmin = 0, Gmax = 255, Gmin = 0,):
	if R == None:
		R = random.randint(Rmin,Rmax)
	if G == None:
		G = random.randint(Gmin,Gmax)
	if B == None:
		B = random.randint(Bmin,Bmax)
	return (R, G, B)