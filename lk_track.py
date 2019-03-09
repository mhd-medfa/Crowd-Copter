#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import video
from common import anorm2, draw_str
from time import clock

lk_params = dict( winSize  = (20,20),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 5 )

class App:
    def __init__(self, video_src):
        self.track_len =10
        self.detect_interval = 5
        self.tracks = []
        self.tracks_and_t = []
        self.cam = video.create_capture(video_src)
        self.frame_idx = 0

    def run(self):
        while True:
            ret, frame = self.cam.read()
            if frame is not None:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_gray = cv2.equalizeHist(frame_gray)
                vis = frame.copy()
                vis1 = frame.copy()
            else:
                return self.tracks_and_t, (self.frame_idx) ,vis1

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                new_track_and_t=[]
                for tr_and_t,tr, (x, y), good_flag in zip(self.tracks_and_t,self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tmpList=list((x,y))
                    tmpList.append(self.frame_idx)
                    tmpTuple=tuple(tmpList)
                    tr_and_t.append(tmpTuple)
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr_and_t[0]
                        del tr[0]
                    new_track_and_t.append(tr_and_t)
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks_and_t = new_track_and_t
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        #look_at_this=self.frame_idx
                        self.tracks.append([(x, y)])
                        self.tracks_and_t.append([(x, y,self.frame_idx)])


            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv2.imshow('lk_track', vis)

            ch = cv2.waitKey(1)
            if ch == 27:
                break

def FindTracks():
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0

    print(__doc__)
    #Tajectories=App(video_src).run()
    cv2.destroyAllWindows()
    return App(video_src).run()
#if __name__ == '__main__':
#    main()
#FindTracks()
