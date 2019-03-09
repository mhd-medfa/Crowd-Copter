import numpy as np

def PairToCluster(pairwiseData, numberOfPoints):

    clusterNumber = 0
    clusterIndex = np.zeros((numberOfPoints), dtype=int)

    for i in range(len(pairwiseData[1])):
        currentPair = np.array([pairwiseData[j][i] for j in range(len(pairwiseData))])
        currentPairAlabel = clusterIndex[currentPair[0]]
        currentPairBlabel = clusterIndex[currentPair[1]]

        if currentPairAlabel==0 and currentPairBlabel==0:
            clusterNumber = clusterNumber+1
            currentPairLabel = clusterNumber
            clusterIndex[currentPair[0]] = currentPairLabel
            clusterIndex[currentPair[1]] = currentPairLabel
        elif currentPairAlabel!=0 and currentPairBlabel==0:
            clusterIndex[currentPair[1]] = currentPairAlabel
        elif currentPairAlabel==0 and currentPairBlabel!=0:
            clusterIndex[currentPair[0]] = currentPairBlabel
        else:
            combineLabel = min(currentPairAlabel, currentPairBlabel)
            indexA=np.asarray(np.nonzero(clusterIndex==currentPairAlabel))
            indexB=np.asarray(np.nonzero(clusterIndex==currentPairBlabel))
            clusterIndex[indexA[0]] = combineLabel
            clusterIndex[indexB[0]] = combineLabel
    newClusterNumber = 0
    for i in range(1,clusterNumber+1):
        currentClusterIndex = np.nonzero(clusterIndex==i)
        if len(currentClusterIndex[0]) < 5:
            '''Remove incoherently moving individuals as the isolated nodes'''
            clusterIndex[currentClusterIndex[0]] = 0
            
        else:
            newClusterNumber = newClusterNumber + 1
            clusterIndex[currentClusterIndex[0]] = newClusterNumber
            
    return clusterIndex
