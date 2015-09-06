# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
        minFinitIndex = 0
        minPnorm = 0
        for i in self.pNorms.keys():
            if abs(self.pNorms[i]) > abs(minPnorm):
                minFinitIndex = i
                minPnorm = self.pNorms[i]
                
        print 
        print "Suurim absoluutne pinge kõrgusel H =", self.H
        print "pNorm = ", self.pNorms[minFinitIndex]
        print "Finit =", self.finits[minFinitIndex].name, ";",
        print "X =", self.finits[minFinitIndex].x, ";",
        print "Y =", self.finits[minFinitIndex].y
  
    def plotSelf(self, title):
        X = np.array([])
        Y = np.array([])
        pNorm = np.array([])
        
        for i in self.finits.keys():
            X = np.append(X, self.finits[i].x)
            Y = np.append(Y, self.finits[i].y)
            pNorm = np.append(pNorm, self.pNorms[i])
            
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(X, Y, pNorm)
        plt.title("%s H = %s" % (title, self.H))
        plt.show()
