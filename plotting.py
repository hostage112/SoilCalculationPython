# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def plotResults(target, title):
    X = np.array([])
    Y = np.array([])
    pNorm = np.array([])

    for i in target.finits.keys():
        X = np.append(X, target.finits[i].x)
        Y = np.append(Y, target.finits[i].y)
        pNorm = np.append(pNorm, target.pNorms[i])

    plt.figure()
    plt.scatter(X, Y, c = pNorm, s=17, edgecolors = 'none', cmap = 'cool')
    plt.title("%s H = %s" % (title, target.H))
    plt.axis('equal')
    plt.colorbar()
    plt.show()

def plotBaseCase(target, title):
    X = np.array([])
    Y = np.array([])
    pNorm = np.array([])

    for i in target.finits.keys():
        X = np.append(X, target.finits[i].x)
        Y = np.append(Y, target.finits[i].y)
        pNorm = np.append(pNorm, target.pNorms[i])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(X, Y, pNorm)
    plt.title("%s H = %s" % (title, target.H))
    plt.show()

def plotFinalResult(New, Old, title):
    nX = np.array([])
    nY = np.array([])
    nPnorm = np.array([])

    for i in New.finits.keys():
        nX = np.append(nX, New.finits[i].x)
        nY = np.append(nY, New.finits[i].y)
        nPnorm = np.append(nPnorm, New.pNorms[i])

    limit = np.amin(nPnorm) * 1.05

    step = New.nodes[1].x - New.nodes[0].x
    nX0 = np.amin(nX)
    nXm = np.amax(nX)
    nXL = nXm - nX0
    shapeX = (nXL / step) + 1
    shapeY = len(nX) / shapeX

    nX = nX.reshape(shapeY, shapeX)
    nY = nY.reshape(shapeY, shapeX)
    nPnorm = nPnorm.reshape(shapeY, shapeX)

    oX = np.array([])
    oY = np.array([])

    for i in Old.nodes.keys():
        oX = np.append(oX, Old.nodes[i].x)
        oY = np.append(oY, Old.nodes[i].y)

    oX0 = np.amin(oX)
    oXm = np.amax(oX)
    oY0 = np.amin(oY)
    oYm = np.amax(oY)

    oContourX = np.array([oX0, oXm])
    oContourY = np.array([oY0, oYm])
    oContourX, oContourY = np.meshgrid(oContourX, oContourY)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(nX, nY, nPnorm)
    ax.plot_surface(oContourX, oContourY, 0, color='red')

    ax.set_zlim(limit, 1)

    plt.title("%s H = %s" % (title, New.H))
    plt.show()
