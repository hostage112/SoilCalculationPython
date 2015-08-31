# -*- coding: utf-8 -*-
import time
import datetime
import classes as data
import work as work

#SETTINGS
Depth = -2.95
deltaDepth = 3.45
case = "test" #"test" #"real"
poisson = 0.35
#SETTINGS

t1 = time.time()

nodes, finits, pNorms = work.importFiles(case)

print
print "Arvutus hakkas:", datetime.datetime.now().time()
print "Arvutus võib võtta ligikaudu:", (len(nodes)*len(finits))/200000/60, "min"

H0 = data.FinitElementData(finits, nodes, Depth)
work.createBaseCase(H0, pNorms)
H0.findMaxPnorm()

Depth -= deltaDepth
H1 = data.FinitElementData(finits, nodes, Depth)
work.generateWestgaard(H1, H0, poisson)
H1.findMaxPnorm()
    
t2 = time.time()
dt = t2 - t1

print
print "Arvutuse võttis aega:", dt/60, "min"