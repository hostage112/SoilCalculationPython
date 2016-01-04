# -*- coding: utf-8 -*-
import math

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

class PlaneData(object):
    def __init__(self, nodes, finits, H):
        self.nodes = nodes
        self.finits = finits
        self.H = H
        self.pNorms = {}

    def findMaxPnorm(self):
        maxFinitIndex = self.pNorms.keys()[0]
        maxPnorm = self.pNorms[maxFinitIndex]
        for i in self.pNorms.keys():
            if abs(self.pNorms[i]) > abs(maxPnorm):
                maxFinitIndex = i
                maxPnorm = self.pNorms[i]

        print "\nMax pressure at H =", self.H
        print "pNorm = ", self.pNorms[maxFinitIndex]
        print "Finit =", self.finits[maxFinitIndex].name, ";",
        print "X =", self.finits[maxFinitIndex].x, ";",
        print "Y =", self.finits[maxFinitIndex].y

        return maxPnorm

    def createBaseCase(self, pNorms):
        self.pNorms = pNorms.copy()
        SelfWeightPressure = 19.0 * self.H

        print
        print "Self weight:", SelfWeightPressure

        for i in pNorms.keys():
            mathPnormValue = pNorms[i] - SelfWeightPressure
            self.pNorms[i] = max(0, mathPnormValue)

        print
        print "Init - done"

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
