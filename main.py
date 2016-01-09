# -*- coding: utf-8 -*- import time import datetime
import time
import datetime

import classes as data
import imports as imp
import plotting as plts

import matplotlib.pyplot as plt

def arvutus():
    #SETTINGS
    depth = 5.220
    deltaDepth = 3.280
    roo = 19.0

    #calculationType = "Boussinesq"
    calculationType = "Westergaard"
    poisson = 0.00

    #TIMER START
    t1 = time.time()
    print "\nCalcualtion start at:", datetime.datetime.now().time()

    #Finits
    robotFinits = imp.importFiles()
    newFinits = data.FinitData.createNewFinits(robotFinits)

    #Existing plane
    H0 = data.PlaneData(robotFinits, depth)
    mx = H0.findMaxPnorm(False)
    plts.plotResults(H0, "Data from Robot", mx)
    H0.calculateEffectivePressure(roo)
    mx = H0.findMaxPnorm(True)
    plts.plotResults(H0, "Effective pressure", mx)

    #New plane
    depth += deltaDepth
    H1 = data.PlaneData(newFinits, depth)
    H1.calculateNewPnormValues(H0, calculationType, poisson)
    H1.findMaxPnorm(True)
    plts.plotResults(H1, calculationType, mx)

    #TIMER END
    t2= time.time()
    print "\nCalculation took:", (t2 - t1)/60, "min"

    #Show all plots
    plt.show()

if __name__ == '__main__':
    arvutus()
