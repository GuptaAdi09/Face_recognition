from PIL import Image, ImageTk
import tkinter as tk
import os.path
import subprocess
import  cv2
from datetime import datetime
import  util




# Replace "resources/NewBack.jpeg" with the actual path to your image
image_path = "resources/modes/Id.jpeg"

def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        web_label.config(image=frame)
        web_label.image = frame
    web_label.after(10, update_video)



# Create the Tkinter root window
root_1 = tk.Tk()

# Load the image and convert it to Tkinter's PhotoImage format
image = Image.open(image_path)
image_tk = ImageTk.PhotoImage(image)

# Resize the window to the image size (optional)
#root_1.geometry(f"{image.width}x{image.height}")
root_1.geometry("1200x720")
# Create a label with the image as background and pack it
label = tk.Label(root_1, image=image_tk)
label.pack(fill="both",side="right")



web_label=tk.Label(root_1,text="webcam",relief="groove",borderwidth=2)
web_label.place(x=10,y=90,width=700,height=500)

cap=cv2.VideoCapture(0)
update_video()








# Define a function for the button click
def button_click():
    root_1.destroy()

    class App:
        def  __init__(self):
            self.main_window=tk.Tk()
            self.main_window.geometry("1200x720")





            self.webcam_label=util.get_img_label(self.main_window)
            self.webcam_label.place(x=10,y=5,width=700,height=600)

            self.add_webcam(self.webcam_label)
            #roll no
            self.Roll_No=util.get_text_label(self.main_window,text="Roll_No")
            self.Roll_No.place(x=720,y=120)
            self.rollno=util.get_entry_text(self.main_window)
            self.rollno.place(x=822,y=120,height=35)
            #class
            self.Class=util.get_text_label(self.main_window,text="Class")
            self.Class.place(x=718,y=180)
            self.get_class=util.get_entry_text(self.main_window)
            self.get_class.place(x=820,y=180,height=35)
            #FullName
            self.fullname=util.get_text_label(self.main_window,text="Name")
            self.fullname.place(x=716,y=230)
            self.get_fullname=util.get_entry_text(self.main_window)
            self.get_fullname.place(x=818,y=230,height=35)
            #DIVISION
            self.div=util.get_text_label(self.main_window,text="Division")
            self.div.place(x=714,y=280)
            self.get_div=util.get_entry_text(self.main_window)
            self.get_div.place(x=816,y=280,height=35)
            #accept button
            self.accept_button_register_new_user_window=util.get_button(self.main_window,"Accept","green",
                                                                 self.accept_register_new_user)
            self.accept_button_register_new_user_window.place(x=814,y=330,height=40)
            #try agin
            self.try_again_button_register_new_user_window=util.get_button(self.main_window,"Try Again",
                                                                           "red",self.try_again_register_new_user)
            self.try_again_button_register_new_user_window.place(x=812,y=380,height=40)

root_1.mainloop()
cap.release()




