import numpy as np

def CoherentFilter_TrackToXV(tracks, currentTime, d):
    tracksSample = tracks[0]
    nDimensions = len(tracksSample[0])-1

    allXset={}
    allVset={}

    for i in range(len(tracks)):
        currentStart = tracks[i][0][2]
        currentEnd  = tracks[i][-1][2]
        if currentTime>currentStart and currentEnd>=(currentTime+d) and len(tracks[i])>=(currentTime+d):
            # Get the points (coordinates and velocity) that is part of Track 'i' and that exist in currentFrame to currentTime + d  frames 
            if nDimensions==2:
                currentX = [[tracks[i][j][0] for j in range((currentTime-currentStart),((currentTime-currentStart)+d))],[tracks[i][j][1] for j in range((currentTime-currentStart),((currentTime-currentStart)+d))]]
                currentV1 = [[tracks[i][j][0] for j in range(((currentTime-currentStart)+1),((currentTime-currentStart)+d+1))],[tracks[i][j][1] for j in range(((currentTime-currentStart)+1),((currentTime-currentStart)+d+1))]]
                currentV2 = [[tracks[i][j][0] for j in range(((currentTime-currentStart)),((currentTime-currentStart)+d))],[tracks[i][j][1] for j in range(((currentTime-currentStart)),((currentTime-currentStart)+d))]]
                currentV = [[(currentV1[0][i]-currentV2[0][i]) for i in range(d)],[(currentV1[1][i]-currentV2[1][i]) for i in range(d)]]
            else:
                currentX = [[tracks[i][j][0] for j in range((currentTime - currentStart), ((currentTime - currentStart) + d - 1))],[tracks[i][j][1] for j in range((currentTime - currentStart), ((currentTime - currentStart) + d - 1))], [tracks[i][j][2] for j in range((currentTime-currentStart),((currentTime-currentStart)+d-1))]]
                currentV1 = [[tracks[i][j][0] for j in range(((currentTime - currentStart) + 1), ((currentTime - currentStart) + d))], [tracks[i][j][1] for j in range(((currentTime - currentStart) + 1), ((currentTime - currentStart) + d))], [tracks[i][j][2] for j in range(((currentTime - currentStart) + 1), ((currentTime - currentStart) + d))]]
                currentV2 = [[tracks[i][j][0] for j in range(((currentTime - currentStart)), ((currentTime - currentStart) + d - 1))], [tracks[i][j][1] for j in range(((currentTime - currentStart)), ((currentTime - currentStart) + d - 1))], [tracks[i][j][2] for j in range(((currentTime - currentStart)), ((currentTime - currentStart) + d - 1))]]
                currentV = [[(currentV1[0][i] - currentV2[0][i]) for i in range(d-1)], [(currentV1[1][i] - currentV2[1][i]) for i in range(d-1)], [(currentV1[2][i] - currentV1[2][i]) for i in range(d-1)]]

            for j in range(d):
                
                if j not in allXset:
                    allXset[j]=[[]]*nDimensions
                    allVset[j]=[[]]*nDimensions
                tmp11 = [[row[j]] for row in currentX]
                if i==0:
                    allXset[j]=tmp11
                else:
                    allXset[j]=[x+y for x,y in zip(allXset[j],tmp11)]

                tmp22 = [[row[j]] for row in currentV]
                if i==0:
                    allVset[j]=tmp22
                else:
                    allVset[j]=[x+y for x,y in zip(allVset[j],tmp22)]

    return allXset, allVset
