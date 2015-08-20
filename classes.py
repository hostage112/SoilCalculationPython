# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

global hhg
hhg = 0

class NodeData(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.pNorm = None
        
    def setpNorm(self, pNorm):
        self.pNorm = pNorm

class FinitData(object):
    def __init__(self, name, x, y, area, corners, pNorm):
        self.name = name
        self.area = area
        self.corners = corners
        self.pNorm = pNorm
        self.x = x
        self.y = y

class FinitElementData(object):
    def __init__(self, H):
        self.name =  np.array([])
        self.pNorm =  np.array([])
        self.area = np.array([])
        self.x = np.array([])
        self.y =  np.array([])
        self.corners = []
        self.H = H

    def generateBlank(self, Other):
        self.name =  Other.name
        self.area = Other.area
        self.x = Other.x
        self.y =  Other.y
        self.corners = Other.corners

    def insertName(self, name):
        self.name = np.append(self.name, name)

    def insertpNorm(self, pNorm):
        self.pNorm = np.append(self.pNorm, pNorm)
        
    def insertArea(self, area):
        self.area = np.append(self.area, area) 
        
    def insertX(self, x):
        self.x = np.append(self.x, x)

    def insertY(self, y):
        self.y = np.append(self.y, y)
        
    def insertCorners(self, corners):
        self.corners.append(corners)   
        
    def generateWestgaard(self, Old, nodes, soil):
        global hhg
        
        def Westergaard(r, v, z, P):
            global hhg
            njuu = (1 - 2 * v) / (2 * (1 - v))
            soilConst = (2 * math.pi)
            distInfluence = ((r / (njuu * z))** 2 + 1) ** (3. / 2)
            sigma = P / (soilConst * (njuu ** 2) * (z ** 2) * distInfluence)
            hhg += 1
            return sigma
        
        def getNodepNorm(self, i, Old):
            sumPnorm = 0
            for j in range(len(self.name)):
                dx = abs(nodes[i].x - self.x[j])
                dy = abs(nodes[i].y - self.y[j])
                r = (dx**2 + dy ** 2) ** (1. / 2)
                P = Old.pNorm[j] * Old.area[j]
                sumPnorm += Westergaard(r, v, dz, P)
            return sumPnorm
        
        v = soil.getPoissonByDepth(self)
        dz = abs(self.H - Old.H)

        for i in nodes.keys():
            nodePnorm = getNodepNorm(self, i, Old)
            nodes[i].setpNorm(nodePnorm)

        for k in range(len(self.name)):
            finitPnorm = 0
            for m in self.corners[k]:
                finitPnorm += nodes[m].pNorm
                
            finitPnorm /= len(self.corners[k])
            self.insertpNorm(finitPnorm)
            
        print hhg    
                
    def findMaxPnorm(self):
        index = 0
        minPnorm = 0
        for i in range(len(self.pNorm)):
            if abs(self.pNorm[i]) > abs(minPnorm):
                index = i
                minPnorm = self.pNorm[i]
                
        print 
        print "Suurim absoluutne pinge kõrgusel H =", self.H
        print "pNorm = ", self.pNorm[index]
        print "Finit =", self.name[index], "; ",
        print "X =", self.x[index], "; ",
        print "Y =", self.y[index]

  
    def plotSelf(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(self.x, self.y, self.pNorm)
        plt.title("H = %s" % (self.H))
        plt.show()             

class SoilData(object):
    def __init__(self):
        self.soilName = np.array([])
        self.depth = np.array([])
        self.poisson = np.array([])
        
    def insertName(self, name):
        self.soilName = np.append(self.soilName, name)
        
    def insertDepth(self, z):
        self.depth = np.append(self.depth, z)
        
    def insertPoisson(self, v):
        self.poisson = np.append(self.poisson, v)

    def getPoissonByDepth(self, H):
        for i in range(len(self.depth)):
            if H > self.depth[i]:
                return self.poisson[i]