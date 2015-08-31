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
    def __init__(self, finits, nodes, H):
        self.finits = finits
        self.nodes = nodes
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
  
    def plotSelf(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(self.x, self.y, self.pNorm)
        plt.title("H = %s" % (self.H))
        plt.show()