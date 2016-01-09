# -*- coding: utf-8 -*-
import os
import csv
import codecs
import classes as data

def importFiles():
    PATH, file = os.path.split(os.path.realpath(__file__))
    NODE = "/nodes.csv"
    FINIT = "/finits.csv"

    nodes = importNodeData(PATH + NODE)
    finits = importFinitElements(nodes, PATH + FINIT)

    print "Imports - done"
    return finits

def importNodeData(PATH):
    nodes = {}

    nodesFile = codecs.open(PATH, 'r', 'utf-16')
    reader = csv.reader(nodesFile, delimiter=';', skipinitialspace=True)
    next(reader, None)

    for row in reader:
        if float(row[3].replace(",", ".")) < 0.001:
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

    finitFile = codecs.open(PATH, 'r', 'utf-16')
    reader = csv.reader(finitFile, delimiter=';', skipinitialspace=True)

    next(reader, None)

    for row in reader:
        name = int(row[0])
        pNorm = float(row[2].replace(",", "."))
        area = float(row[3].replace(",", "."))
        corners = []
        for i in range(4, len(row)):
            try:
                node = int(row[i])
                corners.append(node)
            except:
                pass
        x, y = calculateCenter(corners)

        finits[name] = data.FinitData(name, area, x, y, pNorm)

    finitFile.close()

    return finits
