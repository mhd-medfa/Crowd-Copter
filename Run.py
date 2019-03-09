import cv2
import lk_track
import CoherentFilter
import numpy as np
import matplotlib.pyplot as plt
import random
import dropbox
import datetime

def USER():
    d = 7   # from t -> t+d
    K = 15  # K Nearest Neighbours
    lamda = 0.6 # Threshold
    result = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H-%M-%S") + ".jpg"
    # Get the tracks from KLT algorithm
    trajectories, numberOfFrames, lastFrame = lk_track.FindTracks()
    vis = lastFrame.copy()
    numberOfTracks = len(trajectories)
    trajectories = np.array(trajectories)
    tracksTime = np.zeros((2,numberOfTracks),dtype=int)
    # Get the first and last frame in every track
    for i in range(numberOfTracks):
        tracksTime[0,i] = trajectories[i][0][2] # the first time when each point is appeared
        tracksTime[1,i] = trajectories[i][-1][2] # the last time when each point is appeared
    for i in range(1,numberOfFrames):
        # get the tracks that this frame 'i' is a part of it or a first frame or last frame of it 
        currentIndexTmp1 = np.asarray(np.where(np.in1d(tracksTime[0], [j for j in tracksTime[0] if i>=j])))
        currentIndexTmp2 = np.asarray(np.where(np.in1d(tracksTime[1], [j for j in tracksTime[1] if j>=i])))
        currentIndexTmp1=list(currentIndexTmp1[0])
        currentIndexTmp2=list(currentIndexTmp2[0])
        currentIndex = np.array(list(set(currentIndexTmp1).intersection(set(currentIndexTmp2))))
        includeSet=[trajectories[j] for j in currentIndex]
        '''coherence filtering clustering'''
        currentAllX, clusterIndex = CoherentFilter.CoherentFilter(includeSet, i , d, K, lamda)
        if clusterIndex!=[]:
            numberOfClusters = max(clusterIndex)
            color = np.array([[0,255,128],[0,0,255],[0,255,0],[255,0,0],[255,255,255],[255,255,0],[255,156,0]])
            counter=0
            if i==numberOfFrames-8:
                for x, y in [[np.int32(currentAllX[0][k]),np.int32(currentAllX[1][k])] for k in range(len(currentAllX[0]))]:
                    cv2.circle(lastFrame, (x,y), 5, color[clusterIndex[counter]].tolist(), -1)
                    counter = counter+1
                cv2.imwrite(result, lastFrame)

    cv2.imwrite(result, lastFrame)
    plt.pause(1)
    img = cv2.imread(result)

    ''' uploading the result to Dropbox'''
    im=open(result,'rb')
    f=im.read()
    dbx = dropbox.Dropbox('aWKu0mAkA4AAAAAAAAAADaoI7Tek_2X9cQuQ5op9o_j6fUie8tz3kx9hWIDkAZRx')
    try:
        dbx.files_delete("/"+result)
        dbx.files_upload(f, '/'+result)

    except:
        dbx.files_upload(f, '/'+result)
    print(dbx.files_get_metadata('/'+result).server_modified)

    cv2.imshow(result,img)
    k = cv2.waitKey(0)
    return result


USER()
