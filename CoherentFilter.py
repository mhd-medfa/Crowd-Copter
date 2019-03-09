''' Detecting coherent motion patterns at each frame'''
import numpy as np
import CoherentFilter_TrackToXV
import CoherentFilter_Neighbor
import CoherentFilter_NeighborToPair
import PairToCluster

def CoherentFilter(tracks, currentTime, d, K, lamda):
    '''step1: find K nearest neighbor set at each time'''
    # find position and velocity tracks for each point from t to t+d
    allXset, allVset = CoherentFilter_TrackToXV.CoherentFilter_TrackToXV(tracks, currentTime, d)
    condition=list(allXset)
    if condition!=[]:
        currentAllX = allXset[0]
        numberOfPoints = len(currentAllX[0])
        '''find K nearest neighbor set at each time...'''
        neighborSet, correlationSet = CoherentFilter_Neighbor.CoherentFilter_Neighbor(allXset, allVset, K, d, numberOfPoints)

        '''step2: find the invariant neighbor and pairwise connection set.
           search invariant neighbor and construct the pairwise connections...'''
        pairwiseConnectionSet, correSet = CoherentFilter_NeighborToPair.CoherentFilter_NeighborToPair(neighborSet, correlationSet, d)

        '''step3: threshold pairwise connection set by the averaged correlation
           values, then generate cluster components'''
        '''threshold the average velocity correlations, and get the clustering...'''
        pairwiseConnectionIndex=[index for index,value in enumerate(correSet) if value > lamda]
        includedPairwiseConnectionSet = [[pairwiseConnectionSet[0][x] for x in pairwiseConnectionIndex],[pairwiseConnectionSet[1][x] for x in pairwiseConnectionIndex ] ]
       
        clusterIndex = PairToCluster.PairToCluster(includedPairwiseConnectionSet , numberOfPoints)
        return currentAllX, clusterIndex
    else:
        return [], []
