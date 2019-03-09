import numpy as np
from operator import add

def CoherentFilter_NeighborToPair(neighborSet, correlationSet, d):
    zeroNeighborSet = neighborSet[0]
    numberOfPoints = len(zeroNeighborSet)

    pairwiseConnectionSet = []
    correSet = []

    for i in range(numberOfPoints):
        currentIntersect = zeroNeighborSet[i][:]
        currentCorre=[0]*len(zeroNeighborSet[1])
        for j in range(d):
            nextNeighborSet = neighborSet[j]
            nextCorreSet = correlationSet[j]

            '''the intersection of neighborhood'''
            tmp = list((set(currentIntersect)).intersection(set(nextNeighborSet[i][:])))
            indexA = [currentIntersect.index(c) for c in tmp]
            indexB = [nextNeighborSet[i][:].index(c) for c in tmp]
            currentIntersect = tmp

            currentCorre = list(map(add,[currentCorre[l] for l in indexA], [nextCorreSet[i][l] for l in indexB]))

        if len(currentIntersect) != 0:
            tmp2 = [x / d for x in currentCorre]

            if i==0:
                correSet=tmp2
            else:
                correSet=correSet+tmp2
            tmp3=[[i]*len(currentIntersect),currentIntersect ]

            if i==0:
                pairwiseConnectionSet=tmp3

            else:
                pairwiseConnectionSet=[x+y for x,y in zip(pairwiseConnectionSet,tmp3)]


            # correSet  : averaged velocity set


    return pairwiseConnectionSet, correSet
