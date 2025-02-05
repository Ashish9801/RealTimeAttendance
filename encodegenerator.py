import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("key1.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attend-20d8b-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "attend-20d8b.appspot.com"

})

#importing images

folderPath='Images'
pathList=os.listdir(folderPath)
imgList=[] #contains adresses of images
studentId =[] #Contains all student ids
print(pathList)
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentId.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    #print(os.path.splitext(path)[0])
print(studentId)


def findEndcode(imagelist):
    encodeList=[]
    for img in imagelist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding Started")
encodesListKnown=findEndcode(imgList)
encodingListknownID=[encodesListKnown,studentId]
print("Encoding Complete")

file=open("EncodeFile.p",'wb')
pickle.dump(encodingListknownID,file)
file.close()
print("File Saved")
