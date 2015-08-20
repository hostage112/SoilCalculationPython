# -*- coding: utf-8 -*-
import csv
import codecs
import classes as data

def importSoilData(PATH):

    soilFile = open(PATH, 'r')

    Soil = data.SoilData()    
            
    for row in soilFile:
            splitRow = row.split(";")
            Soil.insertName(int(splitRow[0]))
            Soil.insertDepth(float(splitRow[1]))
            Soil.insertPoisson(float(splitRow[2]))

    soilFile.close()

    return Soil


def importNodeData(PATH):
    nodesFile = codecs.open(PATH, 'r', 'utf-16')
    
    csv.register_dialect('ess', delimiter=';', skipinitialspace=True)
    reader = csv.reader(nodesFile, dialect='ess')
    csv.unregister_dialect('ess')

    nodes = {}
    
    next(reader, None)
    for row in reader:
        if abs(float(row[3].replace(",", "."))) < 0.001:
            name = int(row[0])
            x = float(row[1].replace(",", "."))
            y = float(row[2].replace(",", "."))
            nodes[name] = data.NodeData(name, x, y)
  
    nodesFile.close()
    
    return nodes

def importFinitElements(nodes, PATH):
    def calculateFinitElementCoords(corners):
        midX = 0
        midY = 0

        for node in corners:
            midX += nodes[node].x
            midY += nodes[node].y
            
        midX /= len(corners)
        midY /= len(corners)
            
        return midX, midY

    finitFile = codecs.open(PATH, 'r', 'utf-16')

    csv.register_dialect('ess', delimiter=';', skipinitialspace=True)
    reader = csv.reader(finitFile, dialect='ess')
    csv.unregister_dialect('ess')

    finits = {}

    next(reader, None)

    for row in reader:
        name = int(row[0])
        pNorm = float(row[2].replace(",", ".")) * (-1)
        area = float(row[3].replace(",", "."))
        corners = []
        for i in range(4, len(row)):
            try:
                node = int(row[i])
                corners.append(node)
            except:
                pass
        x, y = calculateFinitElementCoords(corners)
        finits[name] = data.FinitData(name, x, y, area, corners, pNorm)

    finitFile.close()

    return finits


