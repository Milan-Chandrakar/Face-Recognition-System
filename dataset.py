import numpy as np
import cv2
import sqlite3
 
cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def InsertOrUpdate(ID,Name):
    conn = sqlite3.connect('facedata.db')
    cmd = "SELECT * FROM PEOPLE WHERE ID="+str(ID)
    cursor= conn.execute(cmd)
    isRecordexist = 0
    for row in cursor:
        isRecordexist =1
    if (isRecordexist == 1):
        cmd="UPDATE people SET Name=' "+str(Name)+" ' WHERE ID="+str(ID)  
    else:
        cmd="INSERT INTO people(ID,Name) Values("+str(ID)+",' "+str(Name)+" ' )"
    conn.execute(cmd)
    conn.commit()
    conn.close()
    
id = input('id')
Name = input('Name')
InsertOrUpdate(id,Name)
x=0        
 
if cap.isOpened() == False:
    print('Unable to open the camera')
else:
    print('Start grabbing, press a key on Live window to terminate')
    cv2.namedWindow('Live');
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1024)
    while( cap.isOpened() ):
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray,1.1,1)

        for (x,y,w,h) in faces:
            x += 1
            cv2.imwrite('dataSet/user.'+str(id)+'.'+str(x)+'.jpg',gray[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
            
            
        if ret==False:
            print('Unable to grab from the camera')
            break
 
        cv2.imshow('Live',frame)
        #cv2.waitKey(0);
        key = cv2.waitKey(5)
        if key==255: key=-1 #Solve bug in 3.2.0
        if key >= 0:
            break
    print('Closing the camera')
 
cap.release()
cv2.destroyAllWindows()
print('bye bye!')
quit()
