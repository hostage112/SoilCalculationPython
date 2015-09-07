# -*- coding: utf-8 -*-
import time
import datetime
import classes as data
import mesh as mesh
import imports as imp
import plotting as plts

#SETTINGS
case = "test" #"test" #"real"

finitSize = 0.5
calcAreaMultiplier = 1.65

Depth = -2.95
deltaDepth = 3.45

poisson = 0.35
#SETTINGS

t1 = time.time()


print 
print "Calcualtion start at:", datetime.datetime.now().time()   

robotNodes, robotFinits, robotPnorms = imp.importFiles(case)
calcNodes, calcFinits = mesh.generateNewMesh(robotNodes, 
                                            finitSize, calcAreaMultiplier)

H0 = data.FinitElementData(robotNodes, robotFinits, Depth)
H0.createBaseCase(robotPnorms)
H0.findMaxPnorm()
#plts.plotBaseCase(H0, "Data from Robot")

Depth -= deltaDepth

H1 = data.FinitElementData(calcNodes, calcFinits, Depth)
H1.generatePnormValues(H0, "Westergaard", poisson)
H1.findMaxPnorm()
plts.plotFinalResult(H1, H0, "Westergaard")

#H2 = data.FinitElementData(calcNodes, calcFinits, Depth)
#H2.generatePnormValues(H0, "Boussinesq")
##2.findMaxPnorm()
#plts.plotFinalResult(H2, H0, "Boussinesq")


t2= time.time()
dtk = t2 - t1
print
print "Calculations", dtk/60, "min"
