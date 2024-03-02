import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector

cap=cv2.VideoCapture(0)
#imgBG=cv2.imread("resources/NewBack.jpeg")
detector=FaceDetector(minDetectionCon=0.5,modelSelection=0)

while True:
    success,img=cap.read()

    img,bbox=detector.findFaces(img,draw=False)
    #imgBG[161:161+480,46:46+640]=img
    if bbox:
        for bbox in bbox:
            center=bbox["center"]
            x,y,w,h=bbox["bbox"]
            score=int(bbox["score"][0]*100)

            cv2.circle(img,center,5,(255,0,255),cv2.FILLED)
            cvzone.putTextRect(img,f"{score}%",(x, y-10))
            cvzone.cornerRect(img,(x,y,w,h))

    cv2.imshow("Image",img)
    cv2.waitKey(1)
