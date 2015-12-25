# -*- coding: utf-8 -*- import time import datetime
import time
import datetime

import classes as data
import imports as imp
import plotting as plts

import matplotlib.pyplot as plt

def arvutus():
    #SETTINGS
    depth = 5.120
    deltaDepth = 3.580 #3.38 + 0.2 killustiku arvelt

    calculationType = "Westergaard"
    #calculationType = "Boussinesq"
    poisson = 0.0

    #TIMER
    t1 = time.time()
    print "\nCalcualtion start at:", datetime.datetime.now().time()

    #Initialization
    robotNodes, robotFinits, robotPnorms, soils = imp.importFiles()
    calcNodes, calcFinits = robotNodes, robotFinits

    H0 = data.FinitElementData(robotNodes, robotFinits, depth)
    H0.createBaseCase(robotPnorms, soils)

    #Calculation of new plane
    depth += deltaDepth
    H1 = data.FinitElementData(calcNodes, calcFinits, depth)
    H1.generatePnormValues(H0, calculationType, poisson)

    #Results
    H0.findMaxPnorm()
    plts.plotResults(H0, "Data from Robot")

    H1.findMaxPnorm()
    plts.plotResults(H1, calculationType)

    #TIMER
    t2= time.time()
    print "\nCalculation took:", (t2 - t1)/60, "min"
    plt.show()

if __name__ == '__main__':
    arvutus()
