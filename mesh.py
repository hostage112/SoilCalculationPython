# -*- coding: utf-8 -*-
import classes as data
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

def generateNewMesh(robotNodes, finitSize):
    x0 = 0.0
    xm = 0.0
    y0 = 0.0
    ym = 0.0

    for i in robotNodes.keys():
        if robotNodes[i].x < x0:
            x0 = robotNodes[i].x
        if robotNodes[i].x > xm:
            xm = robotNodes[i].x
        if robotNodes[i].y < y0:
            y0 = robotNodes[i].y
        if robotNodes[i].y > ym:
            ym = robotNodes[i].y
      
    dx = abs(xm - x0)
    dy = abs(ym - y0)
    
    print      
    print "old", x0, xm, y0, ym
    print dx, dy
        
    a = 0.1 * dx
    b = 0.1 * dy
    
    modx = (dx + 2*a) % finitSize
    mody = (dy + 2*b) % finitSize
    
    if modx != 0:
        print "täpstustan"
        a += modx/2 + finitSize/2
        modx = (dx + 2*a) % finitSize
    if mody != 0:
        b += mody/2 + finitSize/2
        mody = (dy + 2*b) % finitSize
    
    newX0 = x0 - a
    newY0 = y0 - b
    newXmax = xm + a
    newYmax = ym + b
    
    dx = abs(newXmax - newX0)
    dy = abs(newYmax - newY0)
    
    print
    print "new", newX0, newY0, newXmax, newYmax
    print dx, dy
    print finitSize
    
    X = np.arange(newX0, newXmax+finitSize, finitSize)  
    Y = np.arange(newY0, newYmax+finitSize, finitSize)
    X, Y = np.meshgrid(X, Y)
    P = np.sqrt(X**2 + Y**2)
    
            
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, P, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
    plt.show()