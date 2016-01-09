# -*- coding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt

def plotResults(target, title, mx):
    X = np.array([])
    Y = np.array([])
    pNorm = np.array([])

    mx = int(math.ceil(mx/5.0)) * 5

    for i in target.finits.keys():
        X = np.append(X, target.finits[i].x)
        Y = np.append(Y, target.finits[i].y)
        pNorm = np.append(pNorm, target.finits[i].pNorm)

    plt.figure()
    plt.scatter(X, Y, c = pNorm, s=17, edgecolors = 'none', vmin = -mx, vmax = mx, cmap = 'seismic')
    plt.title("%s H = %s" % (title, target.H))
    plt.axis('equal')
    plt.colorbar()
