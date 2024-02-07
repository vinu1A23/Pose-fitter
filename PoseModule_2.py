# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:23:51 2022

@author: dell
"""

import cv2             # Import OpenCV library for computer vision
import mediapipe as mp # Import Mediapipe library for pose estimation
import time            # Import time library to calculate FPS
import math            # Import math library for mathematical functions

# Defining a class called poseDetector
class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=True, trackCon=True,debugger=False):  
        
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
        self.debugger=debugger
                     
        self.mpDraw = mp. solutions .drawing_utils # Mediapipe drawing utilities 
        self . mpPose = mp.solutions .pose         # Mediapipe pose estimation model
    
        # Initializes the pose model object
        self . pose = self.mpPose . Pose (self. mode, self. upBody, self. smooth,self. detectionCon, self. trackCon) 
    
    #A function FindPose to find relative Landmarks from image
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

    #Define the findPosition to get absolute landmarks - method with parameters for the image and an option to draw
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

                #cx - x-coordinate
                #cy - y-coordinate
                
                cx,cy=int(lm.x*w), int(lm.y*h)
                
                self.lmList.append([id,cx,cy])
                
                if draw or self.debugger:
                    cv2.circle (img, (cx, cy), 5, (255, 0, 0), cv2.FILLED) #draw circle

        #return list of landmarks
        return self.lmList

    #Function findAngle used to find angle between 3 points
    def findAngle(self,img, p1, p2, p3, draw=False) :

        #img - Numpy array of image data
        #p1 - first landmark point
        #p2 - second/mid landmark point
        #p1 - third landmark point
        
        #get the landmark
        x1, y1 = self. lmList [p1] [1:]
        x2, y2 = self. lmList [p2] [1 : ]
        x3, y3 = self. lmList [p3] [1:]
        
        #calculate the angle
        angle= math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2 (y1 - y2, x1 - x2))

        #if angle is negative then angle+360        
        if angle<0:
            angle+=360
        
        if draw or self.debugger:
            
            cv2.line (img, (x1, y1), (x2, y2), (255, 255, 255), 3)   #line between 1st and 2nd point
            cv2.line (img, (x3, y3), (x2, y2), (255, 255, 255), 3)   #line between 3rd and 2nd point
            cv2.circle (img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)  #filled circle on 1st point
            cv2.circle (img, (x1, y1), 15, (0, 0, 255), 2)           #unfilled circle on 1st circle
            cv2.circle (img, (x2, y2), 10, (0, 0, 255), cv2. FILLED) #filled circle on 2nd point
            cv2.circle (img, (x2, y2), 15, (0, 0, 255), 2)           #unfilled circle on 2nd point
            cv2.circle (img, (x3, y3), 10, (0, 0, 255), cv2. FILLED) #filled circle on 3rd point
            cv2.circle (img, (x3, y3), 15, (0, 0, 255), 2)           #unfilled circle on 3rd point
            cv2.putText (img , str(int (angle) ) , (x2 - 50, y2-50),
                         cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)  #print angle on screen
        return angle

    #Function confidence to check visibility of landmarks
    def confidence(self,img,p,draw= True) :

        #img - Numpy array - representation of image
        #p - int - index of landmark for which visibility is to be checked
        #draw - Boolean - True to write on the canvas 

        #return visibility
        return self.results.pose_landmarks.landmark[p].visibility

#Function main to test the functionality of poseDetector class
def main():
    
    #The VideoCapture function can have either value 0 for camera feed or video path or url
    cap = cv2.VideoCapture (" PoseVideos/1.mp4") 
    
    pTime = 0                                      # start time set to 0
    detector = poseDetector()                      # initializing poseDetector Class
    
    while True:
        success, img = cap.read()                  # reading from source for data
        
        if success==False:                         # if no source, print message and exit
            print("no stream ... exiting")
            break
        
        img ,result= detector.findPose(img)        # find relative landmarks from image
        lmList = detector.findPosition (img )      # find absolute position of landmarks
        
        if len (lmList) != 0:                      # Ensure absolute Landmark data is there
            print (lmList [14])                    # printing the 14th landmark point data on console output
            
            #drawing a circle at 14th landmark point
            cv2.circle (img, (lmList [14] [1], lmList [14] [2]), 15, (0, 0, 255), cv2.FILLED) 
             
        cTime = time . time ()                     # time at which frame is being shown
        fps= 1/ (cTime - pTime)                    # fps is frames per second
        pTime = cTime                              # initialize current time as starting time for next frame
        cv2.putText (img, str(int (fps) ), (70, 50), cv2. FONT_HERSHEY_PLAIN,3,
                     (255, 0, 0), 3)               # print the frames per second on canvas
        cv2.imshow("Image", img)                   # show the canvas with final image
        cv2.waitKey (1)                            # pause at key 1

if __name__ == "__main__" :                        # the __main__ namespace
    main ()                                        # run the main function
