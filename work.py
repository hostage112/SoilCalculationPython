# -*- coding: utf-8 -*-
import os
import imports
import math

global calculationSteps
calculationSteps = 0

def importFiles(case):
    PATH, file = os.path.split(os.path.realpath(__file__))
    if (case == "test"):
        NODE = "\\nodes.csv"
        FINIT = "\\finitElements.csv"
    elif (case == "real"):
        NODE = "\\realNodes_05.csv"
        FINIT = "\\realFinits_05.csv"
        
    nodes = imports.importNodeData(PATH + NODE)
    finits, pNorms = imports.importFinitElements(nodes, PATH + FINIT)
    
    print
    print "imports... done"
    return nodes, finits, pNorms

def createBaseCase(Base, pNorms):
    Base.pNorms = pNorms
    
    print    
    print "H0 init... done"
    
def generateWestgaard(New, Old, v):
        
    global calculationSteps
        
    def Westergaard(r, v, z, P):
        global calculationSteps
        njuu = (1 - 2 * v) / (2 * (1 - v))
        soilConst = (2 * math.pi)
        distInfluence = ((r / (njuu * z))** 2 + 1) ** (3. / 2)
        sigma = P / (soilConst * (njuu ** 2) * (z ** 2) * distInfluence)
        calculationSteps += 1
        return sigma
        
    def calculatepNorm(i):
        sumpNorm = 0
        for j in Old.finits.keys():
            dx = abs(New.nodes[i].x - Old.finits[j].x)
            dy = abs(New.nodes[i].y - Old.finits[j].y)
            r = (dx**2 + dy ** 2) ** (1. / 2)
            P = Old.pNorms[j] * Old.finits[j].area
            sumpNorm += Westergaard(r, v, dz, P)
        return sumpNorm
        
    dz = abs(New.H - Old.H)
    nodePnorms = {}

    for i in New.nodes.keys():
        newpNorm = calculatepNorm(i)
        nodePnorms[i] = newpNorm

    for k in New.finits.keys():
        finitPnorm = 0
        for m in New.finits[k].corners:
            finitPnorm += nodePnorms[m]
                
        finitPnorm /= len(New.finits[k].corners)
        New.pNorms[k] = finitPnorm

    print
    print "Arvutus võttis osa:", len(New.nodes), "punkti"
    print "Arvutus võttis:", calculationSteps, "sammu"

    
    
    
    
    