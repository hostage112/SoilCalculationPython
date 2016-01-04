# -*- coding: utf-8 -*-
import math

class NodeData(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class FinitData(object):
    def __init__(self, name, area, corners, x, y, pNorm):
        self.name = name
        self.area = area
        self.corners = corners
        self.x = x
        self.y = y
        self.pNorm = pNorm

    @staticmethod
    def createNewPlane(old):
        new = {}
        for i in old.keys():
            name = old[i].name
            area = old[i].area
            corners = old[i].corners
            x = old[i].x
            y = old[i].y
            pNorm = 0
            new[name] = FinitData(name, area, corners, x, y, pNorm)
        return new

class PlaneData(object):
    def __init__(self, finits, H):
        self.finits = finits
        self.H = H

    def findMaxPnorm(self):
        maxFinitIndex = self.finits.keys()[0]
        maxPnorm = self.finits[maxFinitIndex].pNorm
        for i in self.finits.keys():
            if abs(self.finits[i].pNorm) > abs(maxPnorm):
                maxFinitIndex = i
                maxPnorm = self.finits[i].pNorm

        print "\nMax pressure at H =", self.H
        print "pNorm =", self.finits[maxFinitIndex].pNorm, ";",
        print "Finit =", self.finits[maxFinitIndex].name, ";",
        print "X =", self.finits[maxFinitIndex].x, ";",
        print "Y =", self.finits[maxFinitIndex].y

    def calculateEffectivePressure(self):
        SelfWeightPressure = 19.0 * self.H

        print "Self weight:", SelfWeightPressure

        for i in self.finits.keys():
            mathPnormValue = self.finits[i].pNorm - SelfWeightPressure
            self.finits[i].pNorm = max(0, mathPnormValue)

        print "Init - done"

    def calculateNewPnormValues(self, Old, chosenTheory, v = 0.0):
        def Westergaard(i, j):
            #force
            P = Old.finits[j].pNorm * Old.finits[j].area
            #geometry
            dx = abs(self.finits[i].x - Old.finits[j].x)
            dy = abs(self.finits[i].y - Old.finits[j].y)
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
            P = Old.finits[j].pNorm * Old.finits[j].area
            #geometry
            dx = abs(self.finits[i].x - Old.finits[j].x)
            dy = abs(self.finits[i].y - Old.finits[j].y)
            r = (dx**2 + dy ** 2) ** (1. / 2)
            #influence
            soilConst = 1 / (2 * math.pi)
            distInfluence = 1 / ((1 + (r / dz) ** 2) ** (5. / 2))
            influenceB = 3 * soilConst * distInfluence
            #pressure
            sigma = (P / (dz ** 2)) * influenceB
            return sigma

        def newPnorm(i):
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

        for i in self.finits.keys():
            self.finits[i].pNorm = newPnorm(i)
