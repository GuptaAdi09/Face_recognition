import tkinter as tk
import cv2
from PIL import Image, ImageTk






def main():
    cap = cv2.VideoCapture(0)  # 0 for primary webcam, adjust if needed

    # Function to continuously update the video frame
    def update_video_frame():
        ret, frame = cap.read()
        if ret:
            # Convert frame to PIL Image for Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=frame)
            label.imgtk = imgtk  # Store reference to prevent garbage collection
            label.configure(image=imgtk)
            label.after(10, update_video_frame)
        else:
            # Handle error or stop frame updates if needed
            pass
    # Create Tkinter window, label, and start video updates
    window = tk.Tk()
    window.geometry("700x500")  # Adjust window size as desired
    label = tk.Label(window)
    label.place(x=50,y=0,height=640,width=480)
    update_video_frame()
    #window.mainloop()

def Welcome_frame():
        image_path = "resources/dtssbg.jpeg"
        root_wel = tk.Tk()
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        root_wel.geometry("602x339")
        label = tk.Label(root_wel, image=image_tk)
        label.pack(fill="both", side="right")
        root_wel.title("WELCOME FRAME")

        reg_btn = tk.Button(root_wel, text="Register!!", bg="green",command=main)
        reg_btn.place(x=150, y=250, height=30, width=100)

        log_btn = tk.Button(root_wel, text="Login!!", bg="green")
        log_btn.place(x=300, y=250, height=30, width=100)

        root_wel.mainloop()
Welcome_frame()

