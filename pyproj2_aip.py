# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:38:45 2022

@author: dell
"""

#from pickle import FALSE
import cv2
import numpy as np
import PoseModule_2 as pm
#import tensorflow as tf


class select():
    def __init__(self,detector=pm.poseDetector(),count=0,dir1=1,dir2=1,debugger=False):
        self.detector=pm.poseDetector(debugger=debugger)
        self.count=0
        self.dir1=dir1
        self.dir2=dir2
        self.debugger=debugger
    def start(self,):
        self.count=0
        self.dir1=1
        self.dir2=1
    def c(self,img,p) :
        return self.detector.confidence(img,p)

    #### APPLY GROUND DETECTION for PUSHUP ,BELOW IS POSSIBLE VERTICALLY
    ####SO GROUND DETECTION SHOULD BE HORIZONTAL
    def exerc_1(self,frame):
        
            
        
        """
        success, img=cap.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        """
        img= cv2.resize(frame,(1580,900))
        #img= cv2.imread("img/test.jpg")


        img,result=self.detector.findPose(img)
        #print(result.pose_landmarks.visibility)
        
        # Our operations on the frame come here
        lmList=self.detector.findPosition(img,False)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if len(lmList)!=0:
            """print("hip : ",self.c(24))
            print("elbow : ",self.c(14))
            print("ankle : ", self.c(12))"""
            #left arm
            angle=self.detector.findAngle(img,12,14,16)  #joints in mediapipe
            #right arm
            angle4=self.detector.findAngle(img,11,13,15)
            #left leg
            angle2=self.detector.findAngle(img,24,26,28)
            #right leg        
            angle5=self.detector.findAngle(img,23,25,27)
            #right shoulder and waist and ankle
            angle6=self.detector.findAngle(img,27,23,11)
            angle3=self.detector.findAngle(img,28,24,12)
            """angle3=self.detector.findAngle2(img,14,12,24)
            print("shoulder angle : ",angle3)
            #cv2.putText(img, str(int(angle3)), (int(x2 - 50), int(y2 - 50)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)"""
            per=np.interp(angle,(150,65),(0,100))
            #bar=np.interp(angle,(760,180),(600,100))
            per2=np.interp(angle4,(256,199),(0,100))
            #bar2=np.interp(angle4,(760,180),(600,100))
            
            if 170<= angle2 <=190 and self.c(img,24)>0.9 and self.c(img,26)>0.9 and self.c(img,28) >0.9:
                if per == 100:
                    if self.dir1== 0:
                        self.count += 0.5
                        self.dir1= 1
                if per == 0:
                    if self.dir1== 1:
                        self.count += 0.5
                        self.dir1= 0
                if 170>= angle3 or angle3>=190 :
                    #print("your hip should be in straight alignment with ankle and shoulder")
                    """
                    #update this--------------------
                    if t==0:
                        score-=0.2
                        print("your hip should be in straight alignment with ankle and shoulder")
                    t=1
                    """
            
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


    