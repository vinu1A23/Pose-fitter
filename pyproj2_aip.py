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

            #if back is straight and visibility is high
            if 170 <= angle2 <= 190 and all(self.c(img, i) > 0.9 for i in (24, 26, 28)): 
                if per == 100:                              #if maximum angle that is 65 at right elbow
                    if self.dir1== 0:                       #if direction is relaxing
                        self.count += 0.5                   #count half push up
                        self.dir1= 1                        #change direction to contracting
                        
                if per == 0:                                #if minimum angle that is 150 at right elbow
                    if self.dir1== 1:                       #if direction is contracting
                        self.count += 0.5                   #count half push up
                        self.dir1= 0                        #change direction to relaxing
                        
                if 170>= angle3 or angle3>=190 :
                    print("your hip should be in straight alignment with ankle and shoulder")
                    
            
            elif 163<= angle5 <=171 and self.c(img,23)>0.9 and self.c(img,25)>0.9 and self.c(img,27) >0.9:
                if per2 == 100:
                    if self.dir2 == 0:
                        self.count += 0.5
                        self.dir2 = 1
                if per2 == 0:
                    if self.dir2 == 1:
                        self.count += 0.5
                        self.dir2 = 0
                if 166>= angle6 or angle6>=184 :
                    print("your hip should be in straight alignment with ankle and shoulder")        
            
            #elif 170<= angle2 <=190 and self.c(24)>0.9 and self.c(26)>0.9 and self.c(28) >0.9:
           
            # Draw Bar
            """
            cv2.rectangle (img, (680, 180), (750, 650), (0, 255, 0), 3)
            cv2.rectangle (img, (680, int (bar+60) ) , (750, 550) , (0, 255, 0), cv2.FILLED)
            
            cv2.putText (img, f'self.c(23) {self.c(23)}', (590, 40), cv2. FONT_HERSHEY_PLAIN, 4,
                           (255, 8, 0), 4)
            cv2.putText (img, f'self.c(25) {self.c(25)}', (590, 70), cv2. FONT_HERSHEY_PLAIN, 4,
                           (255, 8, 0), 4)
            cv2.putText (img, f'self.c(27) {self.c(27)}', (590, 90), cv2. FONT_HERSHEY_PLAIN, 4,
                           (255, 8, 0), 4)
            cv2.putText (img, f'angle {angle6}', (590, 140), cv2. FONT_HERSHEY_PLAIN, 4,
                           (255, 8, 0), 4)
            cv2.putText (img, f' {int (per) }%', (500, 75), cv2. FONT_HERSHEY_PLAIN, 4,
                           (255, 8, 0), 4)        
            """         
            cv2.putText (img , str(int (self.count)), (0,100), cv2. FONT_HERSHEY_PLAIN, 5,
                          (255,0,0),10)       
        return img

if __name__=="__main__":
    try:
        sel_exerc=select(debugger=0)
        cap=cv2.VideoCapture(" PoseVideos/1.mp4")
        
        while True:
            success, img=cap.read()
            if not success:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            img=sel_exerc.exerc_1(img)

            cv2.imshow("Image",img)
            key=cv2.waitKey(1)
            if key%256==27:
                break
        cap.release()
        cv2.destroyAllWindows()
    except:
        print("something broke")


    
