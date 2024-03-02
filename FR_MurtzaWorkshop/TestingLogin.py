from PIL import Image, ImageTk
import tkinter as tk
import cv2  # Not used in this part of the code, remove if not needed
import util  # Not used in this part of the code, remove if not needed
import os  # Not used in this part of the code, remove if not needed
import subprocess  # Not used in this part of the code, remove if not needed
import datetime  # Not used in this part of the code, remove if not needed
import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector

class App:


    def  __init__(self):
        image_path = "resources/dtssbg.jpeg"
        self.root_wel = tk.Tk()
        self.root_wel.geometry("602x339")

        # Load and display image
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.root_wel, image=image_tk)
        self.label.pack(fill="both", side="right")

        # Create buttons (assuming they open new frames/functions, not included here)
        self.reg_btn = tk.Button(self .root_wel, text="Register!!", bg="green", command=self.next_window)
        self.reg_btn.place(x=150, y=250, height=30, width=100)

        self.log_btn = tk.Button(self.root_wel, text="Login!!", bg="green",command=self.login_window)
        self.log_btn.place(x=300, y=250, height=30, width=100)
        self.root_wel.mainloop()

    def login_window(self):
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







    def next_window(self):
        self.main_window=tk.Toplevel(self.root_wel)
        self.main_window.geometry("800x700")


        self.register_new_user_main_window=util.get_button(self.main_window,"Capture,My image","green",command=self.register_new_user)

        self.register_new_user_main_window.place(x=130,y=500,height=50,width=500)


        self.image_entry_btn=util.get_entry_text(self.main_window)
        self.image_entry_btn.place(x=320,y=555,height=40,width=400)


        self.webcam_label=util.get_img_label(self.main_window)
        self.webcam_label.place(x=10,y=0,width=700,height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir='./db1'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path="./log.txt"

    def add_webcam(self,label):
        if "cap" not in self.__dict__:
            self.cap=cv2.VideoCapture(0)


        self._label= label
        self.process_webcam()

    def process_webcam(self):
        ret,frame=self.cap.read()
        self.most_recent_capture_arr=frame

        img_=cv2.cvtColor(self.most_recent_capture_arr,cv2.COLOR_RGB2BGR)
        self.most_recent_capture_pil=Image.fromarray(img_)

        imgtk=ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk=imgtk
        self._label.configure(image=imgtk)

        self._label.after(10,self.process_webcam)

    def login(self):
        unknown_img_path="./.temp.jpg"
        cv2.imwrite(unknown_img_path,self.most_recent_capture_arr)

        output=str(subprocess.check_output(["face_recognition",self.db_dir,unknown_img_path]))
        name=output.split(",")[1][:-5]


        if name in ["unknown_person","no_persons_found"]:
           util.msg_box("Oopss....","Unknown User...Please register or try again!")
        else:
           util.msg_box("welcome back!","welcome,{}.".format(name))
           with open(self.log_path,"a")as f:
               f.write("{},{}\n".format(name,datetime.datetime.now()))
               f.close()

        os.remove(unknown_img_path)


    def register_new_user(self):
        self.register_new_user_window=tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x500")

        #roll no
        self.Roll_No=util.get_text_label(self.register_new_user_window,text="Roll_No")
        self.Roll_No.place(x=720,y=120)
        self.rollno=util.get_entry_text(self.register_new_user_window)
        self.rollno.place(x=822,y=120,height=35)
        #class
        self.Class=util.get_text_label(self.register_new_user_window,text="Class")
        self.Class.place(x=718,y=180)
        self.get_class=util.get_entry_text(self.register_new_user_window)
        self.get_class.place(x=820,y=180,height=35)
        #FullName
        self.fullname=util.get_text_label(self.register_new_user_window,text="Name")
        self.fullname.place(x=716,y=230)
        self.get_fullname=util.get_entry_text(self.register_new_user_window)
        self.get_fullname.place(x=818,y=230,height=35)
        #DIVISION
        self.div=util.get_text_label(self.register_new_user_window,text="Division")
        self.div.place(x=714,y=280)
        self.get_div=util.get_entry_text(self.register_new_user_window)
        self.get_div.place(x=816,y=280,height=35)
        #accept button
        self.accept_button_register_new_user_window=util.get_button(self.register_new_user_window,"Accept","green",
                                                                     self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=720,y=380,height=35)
        #try agin
        self.try_again_button_register_new_user_window=util.get_button(self.register_new_user_window,"Try Again",
                                                                               "red",self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=900,y=380,height=35)

        self.capture_label=util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10,y=0,width=700,height=500)

        self.add_img_to_label(self.capture_label)

        '''self.entry_text_register_new_user=util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750,y=150)

        self.text_label_register_new_user=util.get_text_label(self.register_new_user_window,"please,Enter your UserName:")
        self.text_label_register_new_user.place(x=750,y=70)'''

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()


    def add_img_to_label(self,label):
        imgtk=ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk=imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture=self.most_recent_capture_arr.copy()




    def start(self):
        self.main_window.mainloop()



    def accept_register_new_user(self):

        name=self.get_fullname.get(1.0,"end-1c")

        cv2.imwrite(os.path.join(self.db_dir,"{}.png".format(name)),self.register_new_user_capture)

        util.msg_box("SUCCESS","REGISTERED SUCCESSFULLY!!!")
        self.register_new_user_window.destroy()






app = App()
app.start()

