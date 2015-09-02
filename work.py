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
    def Westergaard(i, j):
        #force
        P = Old.pNorms[j] * Old.finits[j].area
        #geometry
        dx = abs(New.nodes[i].x - Old.finits[j].x)
        dy = abs(New.nodes[i].y - Old.finits[j].y)
        r = (dx**2 + dy ** 2) ** (1. / 2)
        #poisson
        njuu = (1 - 2 * v) / (2 * (1 - v))
        #influence
        soilConst = 1 / (2 * math.pi)
        distInfluence = njuu ** (1./2) / ((r / dz) ** 2 + njuu) ** (3./2)
        influenceW = soilConst * distInfluence
        #pressure
        sigma = (P / (dz ** 2)) * influenceW
        return sigma
        
    def partialNodePnorm(i):
        sumPnorm = 0
        for j in Old.finits.keys():
            sumPnorm += Westergaard(i, j)
        return sumPnorm
        
    dz = abs(New.H - Old.H)
    nodePnorms = {}

    for i in New.nodes.keys():
        nodePnorm = partialNodePnorm(i)
        nodePnorms[i] = nodePnorm

    for k in New.finits.keys():
        finitPnorm = 0
        for m in New.finits[k].corners:
            finitPnorm += nodePnorms[m]
                
        finitPnorm /= len(New.finits[k].corners)
        New.pNorms[k] = finitPnorm

def generateBoussinesq(New, Old):
    def Boussinesq(i, j):
        #force
        P = Old.pNorms[j] * Old.finits[j].area
        #geometry
        dx = abs(New.nodes[i].x - Old.finits[j].x)
        dy = abs(New.nodes[i].y - Old.finits[j].y)
        r = (dx**2 + dy ** 2) ** (1. / 2)
        #influence
        soilConst = 1 / (2 * math.pi)        
        distInfluence = 1 / ((1 + (r / dz) ** 2) ** (5. / 2))
        influenceB = 3 * soilConst * distInfluence
        #pressure
        sigma = (P / (dz ** 2)) * influenceB
        return sigma
        
    def partialNodePnorm(i):
        sumPnorm = 0
        for j in Old.finits.keys():
            sumPnorm += Boussinesq(i, j)
        return sumPnorm
        
    dz = abs(New.H - Old.H)
    nodePnorms = {}

    for i in New.nodes.keys():
        nodePnorm = partialNodePnorm(i)
        nodePnorms[i] = nodePnorm

    for k in New.finits.keys():
        finitPnorm = 0
        for m in New.finits[k].corners:
            finitPnorm += nodePnorms[m]
                
        finitPnorm /= len(New.finits[k].corners)
        New.pNorms[k] = finitPnorm 
    