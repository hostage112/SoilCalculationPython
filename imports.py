# -*- coding: utf-8 -*-
import os
import csv
import codecs
import classes as data

def importFiles():
    PATH, file = os.path.split(os.path.realpath(__file__))
    NODE = "/realNodes_05.csv"
    FINIT = "/realFinits_05.csv"
    SOIL = "/realSoil.txt"

    nodes = importNodeData(PATH + NODE)
    finits, pNorms = importFinitElements(nodes, PATH + FINIT)
    soils = importSoilData(PATH + SOIL)

    print "Imports - done"
    return nodes, finits, pNorms, soils

def importNodeData(PATH):
    nodes = {}

    nodesFile = codecs.open(PATH, 'r', 'utf-16')
    reader = csv.reader(nodesFile, delimiter=';', skipinitialspace=True)
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
    def calculateCenter(corners):
        midX = 0
        midY = 0
        for node in corners:
            midX += nodes[node].x
            midY += nodes[node].y
        midX /= len(corners)
        midY /= len(corners)
        return midX, midY

    finits = {}
    pNorms = {}

    finitFile = codecs.open(PATH, 'r', 'utf-16')
    reader = csv.reader(finitFile, delimiter=';', skipinitialspace=True)

    next(reader, None)

    for row in reader:
        name = int(row[0])
        finitPnorm = float(row[2].replace(",", ".")) * (-1)
        area = float(row[3].replace(",", "."))
        corners = []
        for i in range(4, len(row)):
            try:
                node = int(row[i])
                corners.append(node)
            except:
                pass
        x, y = calculateCenter(corners)

        finits[name] = data.FinitData(name, x, y, area, corners)
        pNorms[name] = finitPnorm

    finitFile.close()

    return finits, pNorms

def importSoilData(PATH):
    soils = {}

    soilFile = open(PATH, 'r')

    for row in soilFile:
        splitRow = row.split(";")
        name = int(splitRow[0])
        depth = float(splitRow[1])
        roo = float(splitRow[2])
        soils[name] = data.SoilData(name, depth, roo)

    soilFile.close()

    return soils


