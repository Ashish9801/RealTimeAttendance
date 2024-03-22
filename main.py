import os
import pickle

import cvzone
import numpy as np
import cv2
import face_recognition
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("key1.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attend-20d8b-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "attend-20d8b.appspot.com"

})
bucket = storage.bucket()

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground=cv2.imread("Resourses/background.png")

# import mode images into one list
folderModePath='Resourses/Modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
print (len(imgModeList))

#Load encoding file
print("Loading Encode File")
file=open('EncodeFile.p','rb')
encodeListKnownID=pickle.load(file)
encodeListKnown,studentId=encodeListKnownID
file.close()
print("Encode File Loaded")

modetype=0
count=0
id=-1
imgstudent=[]
while True:
    success,img= cap.read()

    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs-cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

    faceCurr=face_recognition.face_locations(imgs)
    encodeCurr=face_recognition.face_encodings(imgs,faceCurr)

    imgBackground[162 : 162+480,55:55+640]=img
    imgBackground[44: 44 + 633, 808:808 + 414] = imgModeList[modetype]
    if faceCurr:
        for encodeFace, faceLoc in zip(encodeCurr,faceCurr):
            match = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            #print("matches", match)
            #print("faceDis",faceDis)

            matchIndex=np.argmin(faceDis)

            if(match[matchIndex]):
                print("Known face detected")
                print(studentId[matchIndex])
                y1,x2,y2,x1=faceLoc
                y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
                bbox= 55+x1,162+y1,x2-x1,y2-y1
                imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
                id=studentId[matchIndex]
                if count ==0:
                    cvzone.putTextRect(imgBackground,"LOADING",(275,400))
                    cv2.imshow("Attendance",imgBackground)
                    cv2.waitKey(1)
                    count =1
                    modetype=1


    if count !=0:
        if count ==1:
            #Get data from database
            studentInfo=db.reference(f'Students/{id}').get()
            print(studentInfo)
            #Get image from storage
            blob = bucket.get_blob(f'Images/{id}.png')
            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imgstudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            #Update student data
            ref =db.reference(f'Students/{id}')
            studentInfo['total-attendance']+=1
            ref.child('total-attendance').set(studentInfo['total-attendance'])

        if 100<count<200:
            modetype=2
            imgBackground[44: 44 + 633, 808:808 + 414] = imgModeList[modetype]


        if count<=100:
            cv2.putText(imgBackground,str(studentInfo['total-attendance']),(861,125),cv2.FONT_HERSHEY_TRIPLEX,1,(255,255,255),1)

            cv2.putText(imgBackground, str(studentInfo['Major']), (1006, 550), cv2.FONT_HERSHEY_TRIPLEX, 0.5,(255, 255, 255), 1)
            cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_TRIPLEX, 0.5,(255, 255, 255), 1)
            cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_TRIPLEX, 0.6,(100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_TRIPLEX, 0.6,(100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo['Starting-year']), (1125, 625), cv2.FONT_HERSHEY_TRIPLEX, 0.6,(100, 100, 100), 1)
            (w, h), _ = cv2.getTextSize(studentInfo['Name'],cv2.FONT_HERSHEY_TRIPLEX,1,1)
            offset=(414-w)//2
            cv2.putText(imgBackground, str(studentInfo['Name']), (808+offset, 445), cv2.FONT_HERSHEY_TRIPLEX, 1, (50, 50, 50), 1)
            imgBackground[175:175+216,909:909+216]=imgstudent

        count+=1

        if count>=200:
            count=0
            modetype=0
            studentInfo=[]
            imgstudent=[]
            imgBackground[44: 44 + 633, 808:808 + 414] = imgModeList[modetype]



    cv2.imshow("Attendance",imgBackground)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
