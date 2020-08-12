import os 
import cv2  
from PIL import Image
import datetime


def video_from(dirpath, outputfpath="output.avi", fps=30):

    images = [img for img in os.listdir(dirpath)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 

    images.sort(key=lambda x: datetime.datetime.strptime(x, "%H_%M_%S.png"))

    frame = cv2.imread(os.path.join(dirpath, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(outputfpath, 0, fps, (width, height))  

    # Appending the images to the video one by one 
    for i, image in enumerate(images):
        if i>0 and i%300==0: print("wrote 300 frames")
        video.write(cv2.imread(os.path.join(dirpath, image)))

    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()
    video.release()  # releasing the video generated
  
if __name__=="__main__":
    # Calling the generate_video function 
    video_from("snaps/2020_8_11/") 