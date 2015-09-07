# -*- coding: utf-8 -*-
import classes as data
import numpy as np

def generateNewMesh(robotNodes, finitSize, sizeInc):
    def calculateFinitElementCoords(corners):
        midX = 0
        midY = 0

        for node in corners:
            midX += calcNodes[node].x
            midY += calcNodes[node].y
            
        midX /= len(corners)
        midY /= len(corners)
            
        return midX, midY

    foundationX0 = 0.0
    foundationXmax = 0.0
    foundationY0 = 0.0
    foundationYmax = 0.0

    for i in robotNodes.keys():
        if robotNodes[i].x < foundationX0:
            foundationX0 = robotNodes[i].x
        if robotNodes[i].x > foundationXmax:
            foundationXmax = robotNodes[i].x
        if robotNodes[i].y < foundationY0:
            foundationY0 = robotNodes[i].y
        if robotNodes[i].y > foundationYmax:
            foundationYmax = robotNodes[i].y
      
    foundationSizeX = abs(foundationXmax - foundationX0)
    foundationSizeY = abs(foundationYmax - foundationY0)
    
    print
    print "Foundation area size"
    print "X0 =", foundationX0, "Xmax =", foundationXmax,
    print "dX = ", foundationSizeX
    print "Y0 =", foundationY0, "Ymax =", foundationYmax,
    print "dY = ", foundationSizeY

    calcSizeX = foundationSizeX * sizeInc
    calcSizeY = foundationSizeY * sizeInc   

    print
    print "New area size"
    print "calculation X", calcSizeX
    print "calculation Y", calcSizeY
    print

    modx = calcSizeX % finitSize
    mody = calcSizeY % finitSize

    if modx != 0:
        print "Adjust X"
        calcSizeX = calcSizeX - modx + finitSize
        modx = round(calcSizeX % finitSize, 2)
    if mody != 0:
        print "Adjust Y"
        calcSizeY = calcSizeY - mody + finitSize
        mody = round(calcSizeY % finitSize, 2)

    calcX0 = foundationX0 + (foundationSizeX - calcSizeX)/2
    calcY0 = foundationY0 + (foundationSizeY - calcSizeY)/2
    calcXmax = foundationXmax - (foundationSizeX - calcSizeX)/2
    calcYmax = foundationYmax - (foundationSizeY - calcSizeY)/2
    
    print
    print "Calcualtion area size"
    print "calculation X0 =", calcX0, "Xmax =", calcXmax,
    print "dX = ", calcSizeX
    print "calculation Y0 =", calcY0, "Ymax =", calcYmax,
    print "dY = ", calcSizeY    
            
    X = np.arange(calcX0, calcXmax+finitSize, finitSize)  
    Y = np.arange(calcY0, calcYmax+finitSize, finitSize)
    X, Y = np.meshgrid(X, Y)
       
    dy, dx= X.shape
    
    calcNodes = {}
    calcNodesList = [] 
    nodeName = 0
    
    for y in range(dy):
        calcNodeTempList = []
        for x in range(dx):
            tempNodeHolder = data.NodeData(nodeName, X[y, x], Y[y, x])
            calcNodes[nodeName] = tempNodeHolder
            calcNodeTempList.append(tempNodeHolder)
            nodeName += 1
        calcNodesList.append(calcNodeTempList)

    calcFinits = {}
    finitName = 0
    
    for finY in range(dy-1):
        for finX in range (dx-1):
            cor1 = calcNodesList[finY][finX].name
            cor2 = calcNodesList[finY][finX+1].name
            cor3 = calcNodesList[finY+1][finX].name
            cor4 = calcNodesList[finY+1][finX+1].name
            corners = [cor1, cor2, cor3, cor4]
            finitX, finitY = calculateFinitElementCoords(corners)
            area = finitSize ** 2
            calcFinits[finitName] = data.FinitData(finitName, 
                                    finitX, finitY, area, corners)
            finitName += 1            

    print
    print "new mesh generation ... done"

    return calcNodes, calcFinits