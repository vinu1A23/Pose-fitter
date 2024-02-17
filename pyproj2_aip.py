# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:38:45 2022

@author: dell
"""

import cv2                    # import the OpenCV library
import numpy as np            # import the numpy library
import PoseModule_2 as pm     # import PoseModule_2 containing our processing functions

# A class select to select different exercises
class select():

    #Function __init__ to run at creation of class select
    def __init__(self,detector=pm.poseDetector(),count:int=0,dir1:int=1,dir2:int=1,debugger:bool=False)->None:

        #self     - reference to self
        #detector - poseDetector object used to set to a instance of poseDetector class from the PoseModule_2
        #count    - integer used to set count of exercise to 0 by default.
        #dir1     - integer used to set direction for right side. 1 by default
        #dir2     - integer used to set direction for left side. 1 by default
        #debugger - boolean used for debugger state. False by default.

        self.detector=pm.poseDetector(debugger=debugger)
        self.count=0
        self.dir1=dir1
        self.dir2=dir2
        self.debugger=debugger

    #Function start to set initial condition of exercise/ can be used to restart exercise
    def start(self,) -> None:

        #self - reference to self
        self.count=0 # set initial count to 0
        self.dir1=1  # set initial direction for right side to 1
        self.dir2=1  # set initial direction for left side to 1

    #Function c to tell the visibility of the landmark in the image
    def c(self, img:np.ndarray, p:int) -> float:
        return self. detector. confidence(img,p)

    #Function exerc_1 has angle calculations for the pushup and shows the push ups done on screen
    def exerc_1(self,frame:np.ndarray) -> np.ndarray:
        
        #frame - numpy.ndarray used to represent the image data           
        
        img= cv2.resize(frame,(1580,900))                   #resize the image to visible screen size
        
        img,result=self.detector.findPose(img)              #find the relative positions of landmarks
                                                            #image without landmarks drawn is returned 
                                                            #if findpose does not have draw or debugger as True
        
        lmList=self.detector.findPosition(img)              #find the absolute position of the landmarks
        

        if len(lmList)!=0:

            #0 - nose
            #11 - left shoulder
            #12 - right shoulder
            #13 - left elbow
            #14 - right elbow
            #15 - left wrist                                
            #16 - right wrist
            #23 - left hip
            #24 - right hip
            #25 - left knee
            #26 - right knee
            #27 - left ankle
            #28 - right ankle
            #29 - left heel
            #30 - right heel

            
            angle=self.detector.findAngle(img,12,14,16)     #right arm - angle at elbow

            angle4=self.detector.findAngle(img,11,13,15)    #left arm - angle at elbow
            
            angle2=self.detector.findAngle(img,24,26,28)    #right leg - angle at knee
                    
            angle5=self.detector.findAngle(img,23,25,27)    #left leg - angle at knee
            
            angle6=self.detector.findAngle(img,27,23,11)    #left side - angle at hip from ankle and shoulder
            
            angle3=self.detector.findAngle(img,28,24,12)    #right side - angle at hip from ankle and shoulder
            
            per=np.interp(angle,(150,65),(0,100))           #angle at elbow percentage from 0 to 100 for right side
            
            per2=np.interp(angle4,(256,199),(0,100))        #angle at elbow percentage from 0 to 100 for left side            

            #if right leg knee is straight and visibility is high
            if 170 <= angle2 <= 190 and all(self.c(img, i) > 0.9 for i in (24, 26, 28)): 
                
                if per == 100:                              #if maximum contraction angle(65) at right elbow
                    if self.dir1== 0:                       #if direction is relaxing
                        self.count += 0.5                   #count half push up
                        self.dir1= 1                        #change direction to contracting
                        
                if per == 0:                                #if minimum contraction angle(150) at right elbow
                    if self.dir1== 1:                       #if direction is contracting
                        self.count += 0.5                   #count half push up
                        self.dir1= 0                        #change direction to relaxing
                        
                if 170>= angle3 or angle3>=190 :            #if angle at hip from ankle and shoulder is not straight
                    print("your hip should be straight")    #print this message
                    
            #if left leg knee is straight and visibility is high
            elif 163<= angle5 <=171 and all(self.c(img,i) >0.9 for i in (23,25,27)):
                
                if per2 == 100:                             #if maximum contraction angle(199) at left elbow
                    if self.dir2 == 0:                      #if direction is relaxing
                        self.count += 0.5                   #count half push up
                        self.dir2 = 1                       #change direction to contracting
                
                if per2 == 0:                               #if minimum contraction angle(256) at left elbow
                    if self.dir2 == 1:                      #if direction is contracting
                        self.count += 0.5                   #count half push up
                        self.dir2 = 0                       #change direction to relaxing
                
                if 166>= angle6 or angle6>=184 :            #if angle at hip from ankle and shoulder is not straight
                    print("your hip should be in straight") #print this message     
            
            
            cv2.putText(img , str(int (self.count)), (0,100), cv2. FONT_HERSHEY_PLAIN, 5,
                          (255,0,0),10)                     #print the number of push ups done on image
            
        return img                                          #return the processed image

    def exerc_2(self,frame:np.ndarray) -> np.ndarray:
        pass

if __name__=="__main__":                                    #code for testing
    
    try:
        sel_exerc=select(debugger=0)                        #make instance of select class to select exercise
        cap=cv2.VideoCapture("PoseVideos/1.mp4")            #initialize video source
        
        while True:                                         #Read the all the frames in the video source
            success, img=cap.read()                         #Read frames one by one
            if not success:                                 #if the video source has ended or is missing
                print("No frame (stream end?). Exiting")    #print the message to screen and exit
                break                                       #get out of the loop
            
            img=sel_exerc.exerc_1(img)                      #process the image through the push up exercise

            cv2.imshow("Image",img)                         #show the image through windowed screen
            
            key=cv2.waitKey(1)                              #wait for 1 millisecond
            
            if key%256==27:                                 #if ascii 27(escape key) is pressed
                break                                       #get out of loop
        
        cap.release()                                       #release the connection to the video source
        cv2.destroyAllWindows()                             #delete the instances of windowed screens
    
    except:                                                 #if some error occured in above code in some part
        print("something broke")                            #print the error message


    
