import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from db import Attendance,Student
from sqlalchemy import extract
# from PIL import ImageGrab


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name,sess):
    name=name.split('_')[0].lower()
    student=sess.query(Student).filter(Student.name==name).all()
    atd_query=sess.query(Attendance).filter(Attendance.student==student[0].id,
        extract('month', Attendance.taken_on) >= datetime.today().month,
        extract('year', Attendance.taken_on) >= datetime.today().year,
        extract('day', Attendance.taken_on) >= datetime.today().day).all()
    
    if student :
        if len(atd_query)==0:
            atd=Attendance(student=student[0].id)
            sess.add(atd)
            sess.commit()
            sess.close()
            return "attendance taken"
        else:
            return "attendance already taken"
    else:
        return "face not found"

 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
 

def webcam(sess):
    path = 'ImagesAttendance'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    cap = cv2.VideoCapture(0)
    
    while True:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            
            matchIndex = np.argmin(faceDis)
            
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
                result=markAttendance(name,sess)
                if result =="attendance taken":
                    cv2.putText(img,result,(15,15),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),2)
                elif result =='attendance already taken':
                    cv2.putText(img,result,(15,15),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),2)
                elif result =='face not found':
                    cv2.putText(img,result,(15,15),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)
                else:
                    pass
    
        cv2.imshow('Webcam',img)
        if cv2.waitKey(1) ==27:
            break

