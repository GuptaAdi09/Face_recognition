import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin  import storage

cred = credentials.Certificate("ServiceAC.json")
firebase_admin.initialize_app(cred,{

    "databaseURL":"https://facerecognitionattendanc-b78e8-default-rtdb.firebaseio.com/",
     "storageBucket":"facerecognitionattendanc-b78e8.appspot.com"
})

folderPath="db"
PathList=os.listdir(folderPath)
PathList=os.listdir(folderPath)
#print(PathList)

imgList=[]
studentIds=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
    #sending the data (images)to firebase storage
    fileName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentIds)

def findencoding(imagesList):
    encodeList=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("encoding started...")
encodeListKnow=findencoding(imgList)
encodeListKnowwithIds=[encodeListKnow,studentIds]
print("encoding complete")

file=open("EncodeFile.P","wb")
pickle.dump(encodeListKnowwithIds,file)
file.close()
print("file saved")

