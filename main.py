# -*- coding: utf-8 -*-
import os
import time
import imports
import classes as data

def importFiles():
    PATH, file = os.path.split(os.path.realpath(__file__))
    SOIL = "\\soil.txt"
    NODE = "\\realNodes_05.csv"
    FINIT = "\\realFinits_05.csv"
    
    soil = imports.importSoilData(PATH + SOIL)
    nodes = imports.importNodeData(PATH + NODE)
    finits = imports.importFinitElements(nodes, PATH + FINIT)
    return soil, nodes, finits

def createBaseCase(finits, H):
    H0 = data.FinitElementData(H)
    
    for i in finits.keys():
        H0.insertName(finits[i].name)
        H0.insertX(finits[i].x)
        H0.insertY(finits[i].y)
        H0.insertArea(finits[i].area)
        H0.insertCorners(finits[i].corners)
        H0.insertpNorm(finits[i].pNorm + 28)
        
    return H0


t1 = time.time()

Depth = -2.95
deltaDepth = 10 #3.45

soil, nodes, finits = importFiles()
H0 = createBaseCase(finits, Depth)
H0.findMaxPnorm()

Depth -= deltaDepth
H1 = data.FinitElementData(Depth)
H1.generateBlank(H0)
H1.generateWestgaard(H0, nodes, soil)
H1.findMaxPnorm()
    
t2 = time.time()
dt = t2 - t1
print
print "Arvutuse aeg:", dt, "s"

