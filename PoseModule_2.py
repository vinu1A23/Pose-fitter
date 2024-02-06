# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:23:51 2022

@author: dell
"""

import cv2 # Import OpenCV library for computer vision
import mediapipe as mp # Import Mediapipe library for pose estimation
import time # Import time library to calculate FPS
import math # Import math library for mathematical functions
class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=True, trackCon=True,debugger=False):  # Defining a class called poseDetector
        
        #mode - Boolean, uses RGB camera feed if True, BGR otherwise 
        #upBody - Boolean, tracks full body if False, upper body only if True
        #smooth - Boolean, smoothens/filters positions in frames if True
        #detectionCon - Confidence value for detection
        #trackCon - Confidence value for tracking
        #debugger - Boolean, shows debug info if True

        self.mode=mode  
        self.upBody=upBody 
        self.smooth= smooth 
        self. detectionCon = detectionCon 
        self.trackCon = trackCon 
        self.mpDraw = mp. solutions .drawing_utils # Mediapipe drawing utilities 
        self . mpPose = mp.solutions .pose         # Mediapipe pose estimation model
        self . pose = self.mpPose . Pose (self. mode, self. upBody, self. smooth,self. detectionCon, self. trackCon) # Initializes the pose model object
        self.debugger=debugger  
    
    #A function FindPose to find Landmarks from image
    def findPose (self, img, draw=False) :
        
        #img - Numpy array image for which pose landmarks are to be found
        #draw - Boolean draws the landmarks
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convert the image from BGR to RGB color format for processing
        self. results = self. pose . process (imgRGB) #Run the image through the pose estimation model
        
        if self.results . pose_landmarks: 
            #If pose landmarks were detected
            
            if draw or self.debugger: 
                #If set to draw the landmarks or debugger is enabled
                
                self.mpDraw. draw_landmarks (img, self. results .pose_landmarks,self. mpPose . POSE_CONNECTIONS)
        
        return img , self.results.pose_landmarks

    #Define the findPosition method with parameters for the image and an option to draw
    def findPosition (self, img, draw=False) :

        #img - Numpy array image for which pose landmarks are to be found
        #draw - Boolean draws the landmarks
        
        #Initialize an empty list to store landmarks
        self.lmList=[] 
        
        if self.results.pose_landmarks :

            #Iterate through the pose landmarks
            for id, lm in enumerate (self. results . pose_landmarks. landmark):
                
                #id - identity nymber
                #lm - landmark
                
                #h - height
                #w- weight
                
                h, w, c= img.shape
                
                cx,cy=int(lm.x*w), int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw or self.debugger:
                    cv2.circle (img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    
    def findAngle(self,img, p1, p2, p3, draw=False) :
        #get the landmark
        x1, y1 = self. lmList [p1] [1:]
        x2, y2 = self. lmList [p2] [1 : ]
        x3, y3 = self. lmList [p3] [1:]
        #calculate the angle
        angle= math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2 (y1 - y2, x1 - x2))
        if angle<0:
            angle+=360
        
        if draw or self.debugger:
            cv2.line (img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line (img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle (img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle (img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle (img, (x2, y2), 10, (0, 0, 255), cv2. FILLED)
            cv2.circle (img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle (img, (x3, y3), 10, (0, 0, 255), cv2. FILLED)
            cv2.circle (img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText (img , str(int (angle) ) , (x2 - 50, y2-50),
                         cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

    def findAngle2(self, img, p1, p2, p3,draw=False):
        # get the landmark
        x1, z1 = self.results.pose_landmarks.landmark[p1].x, self.results.pose_landmarks.landmark[p1].z
        x2, z2 = self.results.pose_landmarks.landmark[p2].x, self.results.pose_landmarks.landmark[p2].z
        x3, z3 = self.results.pose_landmarks.landmark[p3].x, self.results.pose_landmarks.landmark[p3].z
        y2= self.results.pose_landmarks.landmark[p2].y
        # calculate the angle
        angle = math.degrees(math.atan2(z3 - z2, x3 - x2) - math.atan2(z1 - z2, x1 - x2))
        if angle > 180:
            angle = 360-angle
        cv2.putText(img, str(int(angle)), (int(x2 - 50), int(y2 - 50)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


        return angle
    def confidence(self,img,p,draw= True) :
        return self.results.pose_landmarks.landmark[p].visibility


def main():
    cap = cv2.VideoCapture (" PoseVideos/1.mp4")
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        if success==False:
            print("no stream ... exiting")
            break
        img ,result= detector.findPose(img,False)
        lmList = detector.findPosition (img , draw=False)
        if len (lmList) != 0:
            print (lmList [14])
            cv2.circle (img, (lmList [14] [1], lmList [14] [2]), 15, (0, 0, 255), cv2.FILLED)
        cTime = time . time ()
        fps= 1/ (cTime - pTime)
        pTime = cTime
        cv2.putText (img, str(int (fps) ), (70, 50), cv2. FONT_HERSHEY_PLAIN,3,
                     (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey (1)

if __name__ == "__main__" :
    main () 
