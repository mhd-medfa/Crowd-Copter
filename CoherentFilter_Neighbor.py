import numpy as np
import numpy.matlib

def CoherentFilter_Neighbor(allXset, allVset, K, d, numberOfPoints):

    neighborSet = {}
    correlationSet = {}

    for dd in range(d):
        currentAllX = allXset[dd]
        currentAllV = allVset[dd]
        currentNeighborGraph = np.zeros((numberOfPoints, K), dtype=int)
        currentCorrelationGraph = np.zeros((numberOfPoints, K), dtype=float)

        for i in range(numberOfPoints):
            # Get the point number i
            currentX = [currentAllX[j][i] for j in range(len(currentAllX))]
            currentX = np.array(currentX).reshape(2,1)
            # calculate the distance between current point and other points
            distance = np.subtract(np.matlib.repmat(currentX, 1, numberOfPoints),np.array(currentAllX))
            distance = np.sqrt((distance**2).sum(axis=0))
            # Sort these distances in ascending order
            Index  = np.argsort(distance)

            for KNN in range(K):
                currentV = [currentAllV[j][i] for j in range(len(currentAllV))]
                currentV = np.array(currentV)
                currentKnnV = [currentAllV[j][Index[KNN+1]] for j in range(len(currentAllV))]
                currentKnnV = np.array(currentKnnV)
                if np.sqrt((currentV**2).sum(axis=0))>0 and np.sqrt((currentKnnV**2).sum(axis=0)):
                    # Calculate the correlation between the current point and its neighbours
                    coefficient = np.inner(currentV, currentKnnV)
                    coefficient = coefficient/((np.sqrt((currentV**2).sum(axis=0)))*(np.sqrt((currentKnnV**2).sum(axis=0))))
                    currentNeighborGraph[i][KNN] = Index[KNN+1]
                    currentCorrelationGraph[i][KNN] = coefficient

        if dd not in neighborSet:
            neighborSet[dd] = [[]] * (currentNeighborGraph.shape[0])
            correlationSet[dd] = [[]] * (currentCorrelationGraph.shape[0])

        tmp11 = [list(row) for row in currentNeighborGraph]
        neighborSet[dd] = tmp11

        tmp22 = [list(row) for row in currentCorrelationGraph]
        correlationSet[dd] = tmp22


    return neighborSet, correlationSet
