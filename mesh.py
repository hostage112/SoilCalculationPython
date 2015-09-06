# -*- coding: utf-8 -*-
import classes as data
import numpy as np

def generateNewMesh(robotNodes, finitSize, sizeInc = 1.1):
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
    
    print "foundation X", foundationX0, foundationXmax, foundationSizeX
    print "foundation Y",foundationY0, foundationYmax, foundationSizeY

    calcSizeX = foundationSizeX * sizeInc
    calcSizeY = foundationSizeY * sizeInc   

    print "calculation X", calcSizeX
    print "calculation Y", calcSizeY

    modx = calcSizeX % finitSize
    mody = calcSizeY % finitSize

    if modx != 0:
        print "täpstustan X"
        calcSizeX = calcSizeX - modx + finitSize
        modx = round(calcSizeX % finitSize, 2)
    if mody != 0:
        print "täpstustan Y"
        calcSizeY = calcSizeY - mody + finitSize
        mody = round(calcSizeY % finitSize, 2)

    calcX0 = foundationX0 + (foundationSizeX - calcSizeX)/2
    calcY0 = foundationY0 + (foundationSizeY - calcSizeY)/2
    calcXmax = foundationXmax - (foundationSizeX - calcSizeX)/2
    calcYmax = foundationYmax - (foundationSizeY - calcSizeY)/2
    
    print "calculation X", calcX0, calcXmax, calcSizeX
    print "calculation Y", calcY0, calcYmax, calcSizeY
    
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

    return calcNodes, calcFinits