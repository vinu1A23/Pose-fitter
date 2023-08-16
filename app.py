from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys

from threading import Thread
import pyproj2_aip as fitter


global capture,rec_frame, switch, rec, out, Exer
capture=0

Exer=0
switch=1
rec=0
rec_frame=False

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
#net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

#making instance of class from scorer and debugger
selector=fitter.select(debugger=False).exerc_1 


camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        #print(rec)
        time.sleep(0.05)
        out.write(rec_frame)


def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
          
            
            if(Exer):
                
                frame=selector(cv2.flip(frame,1))
                frame=cv2.flip(frame,1)
               
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        
        elif  request.form.get('Exer') == 'Exer':
            global Exer
            Exer=not Exer
        
        
        elif request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')
    

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True)
    
    