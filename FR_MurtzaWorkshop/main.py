import os
import pickle
import cvzone
import cv2
import face_recognition
import numpy as np
from datetime import datetime
import time
from datetime import timezone
import pytz

from cvzone.FaceDetectionModule import FaceDetector
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin  import storage
import numpy as np

import util







current_time = datetime.now(timezone.utc)
local_time = current_time.astimezone()
print(f"Current time in UTC: {current_time}")
print(f"Local time: {local_time}")
print(f"Time zone: {local_time.tzname()}")


cred = credentials.Certificate("ServiceAC.json")
firebase_admin.initialize_app(cred,{

    "databaseURL":"https://facerecognitionattendanc-b78e8-default-rtdb.firebaseio.com/",
     "storageBucket":"facerecognitionattendanc-b78e8.appspot.com"
})

bucket=storage.bucket()
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

#importing the mode images into list


imgBG=cv2.imread("resources/NewBack.jpeg")
folderModePath="resources/modes"
modePathList=os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#print(len(imgModeList))
#load the encoding file
print("Loading Encoding file")
file=open("EncodeFile.P","rb")
encodeListKnowwithIds=pickle.load(file)
file.close()
encodeListKnow,studentIds=encodeListKnowwithIds
#print(studentIds)
print("encoded file load")
detector=FaceDetector(minDetectionCon=0.5,modelSelection=0)
modeType=2
counter=0
id=-1
imgStudent=[]




while True:
    success,img=cap.read()

    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)


    imgBG[161:161+480,46:46+640]=img
    imgBG,bbox=detector.findFaces(imgBG,draw=False)
    imgBG[25:25+676,805:805+465]=imgModeList[modeType]


    for encodeFace ,faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnow,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnow,encodeFace)

        #print("matches",matches)
        #print("faceDistance",faceDis)

        matchIndex=np.argmin(faceDis)
        #print("match index",matchIndex)
        if matches[matchIndex]:
            if bbox:
                for bbox in bbox:
                    center=bbox["center"]
                    x,y,w,h=bbox["bbox"]
                    score=int(bbox["score"][0]*100)

                    cv2.circle(imgBG,center,5,(255,0,255),cv2.FILLED)
                    cvzone.putTextRect(imgBG,f"{score}%",(x, y-10))
                    cvzone.cornerRect(imgBG,(x,y,w,h))
                    id=studentIds[matchIndex]
                    #print(id)
            id=studentIds[matchIndex]
                    #print(id)
            if counter==0:
                counter=1
                modeType=2

    if counter!=0:
        if counter==1:
            #get the data
            studetsInfo=db.reference(f"students/{id}").get()
            print(studetsInfo)

            # Get the blob from Firebase Storage

            blob=bucket.get_blob(f"resources/images/{id}.png")
            print(f"Value of blob before download: {blob}")

            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            ref=db.reference(f"students/{id}")
            ref.child("total_attendance").transaction(lambda current_value: (current_value or 0) + 1)





            #stored_datetime=studetsInfo["last_attendance_time"]
            '''ref=db.reference(f"students/{id}")
            last=ref.child("last_attendance_time").get()
            last_attendance_time = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")

            current_time=datetime.now(timezone.utc)

            time_difference=current_time-last
            second_only=time_difference.total_seconds()
            print(f"time difference:{second_only}")'''
            '''if second_only>30:
                ref=db.reference(f"students/{id}")
                ref.child("total_attendance").transaction(lambda current_value: (current_value or 0) + 1)
                #setting the last attendance time as current time

                now_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ref.child("last_attendance_time").set(now_str)'''
            '''else:
                modeType=1
                counter=0
                imgBG[25:25+676,805:805+465]=imgModeList[modeType]'''

        if modeType !=1:
            if 10<counter<20:
                   modeType=3

            imgBG[25:25+676,805:805+465]=imgModeList[modeType]

            if counter<=10:
                    cv2.putText(imgBG,str(studetsInfo["total_attendance"]),(880,145),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)
                    cv2.putText(imgBG,str(studetsInfo["FullName"]),(910,520),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.9,(0,0,0),1)
                    cv2.putText(imgBG,str(studetsInfo["Class"]),(910,560),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.9,(0,0,0),1)
                    cv2.putText(imgBG,str(studetsInfo["Roll_No"]),(950,607),cv2.FONT_HERSHEY_TRIPLEX,0.8,(0,0,0),1)
                    cv2.putText(imgBG,str(studetsInfo["Division"]),(950,645),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)

                    # Calculate available space and determine scaling factor
                    max_width = 1280 - 909  # Right corner available width
                    max_height = 720 - 175  # Top available height

                    # Calculate the maximum possible width and height the image can have while
                    # still fitting within the available space and maintaining aspect ratio
                    max_possible_width = min(max_width, imgStudent.shape[1])
                    max_possible_height = min(max_height, imgStudent.shape[0])

                    # Calculate the scale factor based on the maximum possible dimensions
                    scale_factor = min(max_possible_width / imgStudent.shape[1], max_possible_height / imgStudent.shape[0])

                    # Resize the image to fit while maintaining aspect ratio
                    resized_img = cv2.resize(imgStudent, None, fx=scale_factor, fy=scale_factor)

                    # Calculate the top-left corner coordinates for placement in the top right corner
                    top_left_x = 1280 - resized_img.shape[1]-130 # Rightmost coordinate minus image width
                    top_left_y = 175  # Topmost coordinate

                    # Overlay the resized image onto the background frame
                    imgBG[top_left_y:top_left_y + resized_img.shape[0],
                          top_left_x:top_left_x + resized_img.shape[1]] = resized_img

        counter += 1

        if counter>=20:
            counter=0
            modeType=0
            studetsInfo=[]
            imgStudent=[]
            imgBG[25:25+676,805:805+465]=imgModeList[modeType]


    cv2.imshow("Face",imgBG)
    cv2.waitKey(1)






