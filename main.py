# -*- coding: utf-8 -*-
import time
import datetime
import classes as data
import work as work

#SETTINGS
Depth = -2.95
deltaDepth = 3.45
case = "real" #"test" #"real"
poisson = 0.35
#SETTINGS

t1 = time.time()

nodes, finits, pNorms = work.importFiles(case)

print
print "Arvutus hakkas:", datetime.datetime.now().time()
print "Arvutus võib võtta ligikaudu:", (len(nodes)*len(finits))/200000/60, "min"
print len(nodes)

H0 = data.FinitElementData(finits, nodes, Depth)
work.createBaseCase(H0, pNorms)
H0.findMaxPnorm()
H0.plotSelf("Base")

Depth -= deltaDepth
"""
H1_west1 = data.FinitElementData(finits, nodes, Depth)
work.generateWestgaard(H1_west1, H0, 0.0)
H1_west1.findMaxPnorm()

H1_west2 = data.FinitElementData(finits, nodes, Depth)
work.generateWestgaard(H1_west2, H0, 0.1)
H1_west2.findMaxPnorm()

H1_west3 = data.FinitElementData(finits, nodes, Depth)
work.generateWestgaard(H1_west3, H0, 0.2)
H1_west3.findMaxPnorm()

H1_west4 = data.FinitElementData(finits, nodes, Depth)
work.generateWestgaard(H1_west4, H0, 0.3)
H1_west4.findMaxPnorm()
"""
H1_west5 = data.FinitElementData(finits, nodes, Depth)
work.generateWestgaard(H1_west5, H0, 0.35)
H1_west5.findMaxPnorm()

H1_bouss = data.FinitElementData(finits, nodes, Depth)
work.generateBoussinesq(H1_bouss, H0)
H1_bouss.findMaxPnorm()

t2 = time.time()
dt = t2 - t1

print
print "Arvutuse võttis aega:", dt/60, "min"