'''import cv2
import os
from PIL import Image

folderPath="db1"
PathList=os.listdir(folderPath)
for image in PathList :
    img=cv2.imread("db1/helo.png")
    original_width, original_height = img.shape[:2]
    aspect_ratio = original_width / original_height
    # Choose the target dimension that preserves the aspect ratio
    if aspect_ratio > 1:  # Wider image, prioritize target width
        new_width = 216
        new_height = int(new_width / aspect_ratio)
    else:  # Taller image, prioritize target height
        new_height = 228
        new_width = int(new_height * aspect_ratio)

    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    cv2.imwrite("resized_image.jpg", resized_img)
    # Or
    cv2.imshow("Resized Image", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

import  os
from PIL import  Image
import cv2

folder_path="db1"
resized_directory="./resisizeDB"
if not os.path.exists(resized_directory):
    os.mkdir(resized_directory)

resized_folder_path=resized_directory
def resize_image(img,new_size):
    return img.resize(new_size,Image.ANTIALIAS)

for filename in os.listdir(folder_path):
    if filename.endswith((".jpg","jpeg",".png")):
        image_path=os.path.join(folder_path,filename)
        image=Image.open(image_path)

        resized_image=cv2.resize(image,(216,288))

        resized_filename=f"{resized_folder_path}/{filename}"
        print(f"Resizes Image Saved:{resized_filename}")





