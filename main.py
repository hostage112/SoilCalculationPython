# -*- coding: utf-8 -*-
import time
import datetime
import classes as data
import work as work
import mesh as mesh

#SETTINGS
case = "test" #"test" #"real"

finitSize = 0.5
calcAreaMultiplier = 2.0

Depth = -2.95
deltaDepth = 3.45

poisson = 0.35
#SETTINGS

t1 = time.time()

robotNodes, robotFinits, robotPnorms = work.importFiles(case)
calcNodes, calcFinits = mesh.generateNewMesh(robotNodes, 
                                            finitSize, calcAreaMultiplier)
print
print "Arvutus hakkas:", datetime.datetime.now().time()
print "Arvutus võib võtta ligikaudu:", (len(calcNodes)*len(robotNodes))/200000/60, "min"
print len(calcNodes)

H0 = data.FinitElementData(robotNodes, robotFinits, Depth)
work.createBaseCase(H0, robotPnorms)
H0.findMaxPnorm()
H0.plotSelf("Base")

Depth -= deltaDepth

H1 = data.FinitElementData(calcNodes, calcFinits, Depth)
work.generateWestgaard(H1, H0, poisson)
H1.findMaxPnorm()
H1.plotSelf("west", + poisson)

H2 = data.FinitElementData(calcNodes, calcFinits, Depth)
work.generateBoussinesq(H2, H0)
H2.findMaxPnorm()
H2.plotSelf("bouss")

t2 = time.time()
dt = t2 - t1

print
print "Arvutuse võttis aega:", dt/60, "min"
