from PIL import Image, ImageTk
import tkinter as tk
import cv2
import util
import os
import subprocess
import datetime








def Welcome_frame():
        image_path = "resources/dtssbg.jpeg"
        global root_1,cap,web_label

        root_wel = tk.Tk()
        root_1=root_wel
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        root_wel.geometry("602x339")
        label = tk.Label(root_wel, image=image_tk)
        label.pack(fill="both", side="right")
        root_wel.title("WELCOME FRAME")

        reg_btn = tk.Button(root_wel, text="Register!!", bg="green")
        reg_btn.place(x=150, y=250, height=30, width=100)

        log_btn = tk.Button(root_wel, text="Login!!", bg="green")
        log_btn.place(x=300, y=250, height=30, width=100)

        root_wel.mainloop()

Welcome_frame()





