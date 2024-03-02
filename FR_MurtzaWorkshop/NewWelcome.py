from PIL import Image, ImageTk
import tkinter as tk
import cv2  # Not used in this part of the code, remove if not needed
import util  # Not used in this part of the code, remove if not needed
import os  # Not used in this part of the code, remove if not needed
import subprocess  # Not used in this part of the code, remove if not needed
import datetime  # Not used in this part of the code, remove if not needed


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
        '''self.login=tk.Toplevel(self.root_wel)
        self.login.geometry("620x339")
        self.log_btn = tk.Button(self.login, text="Login!!", bg="green")
        self.log_btn.place(x=300, y=250, height=30, width=100)
        self.login.mainloop()'''




    def next_window(self):
        self.main_window=tk.Toplevel(self.root_wel)
        self.main_window.geometry("800x600")

        '''self.login_button_main_window=util.get_button(self.main_window,"login","green",self.login)
        self.login_button_main_window.place(x=750,y=300)'''

        self.register_new_user_main_window=util.get_button(self.main_window,"Capture,My image","green",
                                                           self.register_new_user)
        self.register_new_user_main_window.place(x=130,y=500,height=50,width=500)


        self.webcam_label=util.get_img_label(self.main_window)
        self.webcam_label.place(x=10,y=0,width=700,height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir='./db'
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
        name=self.entry_text_register_new_user.get(1.0,"end-1c")
        cv2.imwrite(os.path.join(self.db_dir,"{}.jpg".format(name)),self.register_new_user_capture)

        util.msg_box("SUCCESS","REGISTERED SUCCESSFULLY!!!")
        self.register_new_user_window.destroy()




app = App()
app.start()

