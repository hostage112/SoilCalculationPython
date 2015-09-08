# -*- coding: utf-8 -*-
import time
import datetime
import classes as data
import mesh as mesh
import imports as imp
import plotting as plts

#SETTINGS
case = "real" #"test" #"real"
thoery = "Westergaard" #"Boussinesq" "Westergaard"

finitSize = 0.5
calcAreaMultiplier = 1.6

depthSetting = 5.05
deltaDepth = 3.45

if case == "test":
    waterDepth = 0.0
elif case == "real":
    waterDepth = 2.25

poisson = 0.35
#SETTINGS

t1 = time.time()

print 
print "Calcualtion start at:", datetime.datetime.now().time()   

robotNodes, robotFinits, robotPnorms, soils = imp.importFiles(case)
calcNodes, calcFinits = mesh.generateNewMesh(robotNodes, 
                                            finitSize, calcAreaMultiplier)

#NORMAL CALCULATION
Depth = depthSetting

H0 = data.FinitElementData(robotNodes, robotFinits, Depth)
H0.createBaseCase(robotPnorms, soils, waterDepth)
H0.findMaxPnorm()
plts.plotBaseCase(H0, "Data from Robot")

Depth += deltaDepth

#H1 = data.FinitElementData(calcNodes, calcFinits, Depth)
#H1.generatePnormValues(H0, thoery, poisson)
#H1.findMaxPnorm()
#plts.plotFinalResult(H1, H0, thoery)

#LESS WATER CALCULATION
Depth = depthSetting
waterDepth -= 1

HH0 = data.FinitElementData(robotNodes, robotFinits, Depth)
HH0.createBaseCase(robotPnorms, soils, waterDepth)
HH0.findMaxPnorm()
plts.plotBaseCase(HH0, "Data from Robot")

Depth += deltaDepth

HH1 = data.FinitElementData(calcNodes, calcFinits, Depth)
HH1.generatePnormValues(HH0, thoery, poisson)
HH1.findMaxPnorm()
plts.plotFinalResult(HH1, HH0, thoery)

HH2 = data.FinitElementData(calcNodes, calcFinits, Depth)
HH2.generatePnormValues(HH0, "Boussinesq", poisson)
HH2.findMaxPnorm()
plts.plotFinalResult(HH2, HH0, "Boussinesq")

t2= time.time()
dtk = t2 - t1
print
print "Calculations", dtk/60, "min"
