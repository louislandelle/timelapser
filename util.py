import os 
import cv2  
from PIL import Image
import datetime


def fetch_cam_res2():
    # Returns list of available camera resolutions for current webcam

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1e7)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1e7)

    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cv2.destroyAllWindows()
    del(camera)

    return width, height

def fetch_cam_res():
    # Returns list of available camera resolutions for current webcam

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(0)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')

    available = []
    for i in range(11):
        print("querying width", i*200)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, i*200)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if not (width, height) in available:
            available.append((width, height))

    cv2.destroyAllWindows()
    del(camera)

    print(available)
    return available

def video_from(dirpath, outputfpath="output.avi", fps=30):
    # Creates a video from directory with frames and provided fps, supports JPEG and PNG

    formats = ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG"]

    images = [img for img in os.listdir(dirpath) if any(img.endswith(fmt) for fmt in formats)]
    
    def _key(x):
        def _trymatch(formats, idx):
            if idx >= len(formats):
                raise Exception("File couldn't match available format.")
            try:
                return datetime.datetime.strptime(x, "%H_%M_%S." + formats[idx])
            except ValueError:
                return _trymatch(formats, idx+1)
        
        return _trymatch(formats, 0)

    images.sort(key=lambda x: _key(x))

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
    #video_from("snaps/2020_8_11/") 
    fetch_cam_res()