# -*- coding: utf-8 -*-
import math 

class SoilData(object):
    def __init__(self, name, depth, roo):
        self.name = int(name)
        self.depth = float(depth)
        self.roo = float(roo)

class NodeData(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class FinitData(object):
    def __init__(self, name, x, y, area, corners):
        self.name = name
        self.area = area
        self.corners = corners
        self.x = x
        self.y = y

class FinitElementData(object):
    def __init__(self, nodes, finits, H):
        self.nodes = nodes
        self.finits = finits
        self.H = H
        self.pNorms = {}
                      
    def findMaxPnorm(self):
        minFinitIndex = self.pNorms.keys()[0]
        minPnorm = self.pNorms[minFinitIndex]
        for i in self.pNorms.keys():
            if abs(self.pNorms[i]) > abs(minPnorm):
                minFinitIndex = i
                minPnorm = self.pNorms[i]
                
        print 
        print "Max pressure at H =", self.H
        print "pNorm = ", self.pNorms[minFinitIndex]
        print "Finit =", self.finits[minFinitIndex].name, ";",
        print "X =", self.finits[minFinitIndex].x, ";",
        print "Y =", self.finits[minFinitIndex].y

    def createBaseCase(self, pNorms, soils, waterDepth):
        self.pNorms = pNorms.copy()
        
        SelfWeightPressure = 0.0
        
        waterPressure = (self.H - waterDepth) * 10
        if waterPressure < 0:
            waterPressure = 0
            
        lastSoil = SoilData(0, 0.0, 0.0)
        
        def getSelfWeightPressure(soil, lastSoil):
            deltaDepth = soil.depth - lastSoil.depth
            
            if soil.depth <= waterDepth:
                return soil.roo * deltaDepth
            
            if lastSoil.depth >= waterDepth:
                return (soil.roo - 10) * deltaDepth
                       
            withoutWaterDelta = waterDepth - lastSoil.depth
            withWaterDelta = soil.depth - waterDepth
            
            argRoo = (withoutWaterDelta * soil.roo + withWaterDelta * (soil.roo - 10)) / (deltaDepth)
            return argRoo * deltaDepth
        
        for i in soils.keys():
            if soils[i].depth < self.H:
                SelfWeightPressure += getSelfWeightPressure(soils[i], lastSoil)
            else:
                currentSoil = SoilData(777, self.H, soils[i].roo)
                SelfWeightPressure += getSelfWeightPressure(currentSoil, lastSoil)
                break
            lastSoil = soils[i]
        
        print 
        print "Self:", SelfWeightPressure, "Water:", waterPressure
                
        for i in pNorms.keys():
            mathPnormValue = pNorms[i]+ waterPressure + SelfWeightPressure
            if mathPnormValue > 0:
                self.pNorms[i] = 0
            else:
                self.pNorms[i] = mathPnormValue
               
        print    
        print "H0 init... done"

    def generatePnormValues(self, Old, chosenTheory, v = 0.0):
        def Westergaard(i, j):
            #force
            P = Old.pNorms[j] * Old.finits[j].area
            #geometry
            dx = abs(self.nodes[i].x - Old.finits[j].x)
            dy = abs(self.nodes[i].y - Old.finits[j].y)
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
        
        def Boussinesq(i, j):
            #force
            P = Old.pNorms[j] * Old.finits[j].area
            #geometry
            dx = abs(self.nodes[i].x - Old.finits[j].x)
            dy = abs(self.nodes[i].y - Old.finits[j].y)
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
                if chosenTheory == "Westergaard":
                    sumPnorm += Westergaard(i, j)
                elif chosenTheory == "Boussinesq":
                    sumPnorm += Boussinesq(i, j)
                else:
                    raise ValueError
            return sumPnorm
            
        dz = abs(self.H - Old.H)
        nodePnorms = {}
           
        for i in self.nodes.keys():
            nodePnorm = partialNodePnorm(i)
            nodePnorms[i] = nodePnorm
    
        for k in self.finits.keys():
            finitPnorm = 0
            for m in self.finits[k].corners:
                finitPnorm += nodePnorms[m]
                    
            finitPnorm /= len(self.finits[k].corners)
            self.pNorms[k] = finitPnorm