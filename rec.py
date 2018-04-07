import cv2
import sqlite3

rec = cv2.face.createLBPHFaceRecognizer()
rec.load('recognizer/traindata.yml')
face = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
path = 'dataSet'

def getProfile(id) :
    conn = sqlite3.connect('facedata.db')
    cmd = "SELECT * FROM PEOPLE WHERE ID="+str(id)
    cursor= conn.execute(cmd)
    profile = None
    for row in cursor :
        profile = row
    conn.close()
    return profile

cap = cv2.VideoCapture(0)
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('output.avi', fourcc, 20, (320,240))
font = cv2.FONT_HERSHEY_SIMPLEX

if cap.isOpened() == False:
    print('Unable to open the camera')
else:
    print('Start grabbing, press a key on Live window to terminate')
    cv2.namedWindow('Live')
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    while( cap.isOpened() ):
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray,1.1,1)

        for (x,y,w,h) in faces:
            id, conf = rec.predict(gray[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            profile = getProfile(id)
            print(id,conf)
            if (profile != None):
                cv2.putText(frame,str(profile[1]),(x,y+h+30),font,1,(255,255,0),2)
            else :
                cv2.putText(frame,'unknown',(x,y+h+30),font,1,(255,255,0),2)
        cv2.imshow('Live',frame)
        #out.write(frame)
        
        
        key = cv2.waitKey(5)
        if key==255: key=-1 
        if key >= 0:
            break
    print('Closing the camera')
 
cap.release()
cv2.destroyAllWindows()
print('bye bye!')
quit()        
                
            
