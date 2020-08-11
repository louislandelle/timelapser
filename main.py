import cv2
import time
import datetime
from pathlib import Path

camera = cv2.VideoCapture(0)
curr_d = None
curr_folder = None
while ...:

    t = datetime.datetime.now()

    if curr_d != (t.year, t.month, t.day):
        curr_d = (t.year, t.month, t.day)
        print("Changed day to", curr_d)
        curr_folder = "snaps/"+'_'.join(str(_) for _ in curr_d)
        Path(curr_folder).mkdir(parents=True, exist_ok=True)

    ret_val, img = camera.read()
    t = datetime.datetime.now()
    if t.second % 30 == 0:
        cv2.imwrite(curr_folder + '/' + '_'.join(str(_) for _ in (t.hour, t.minute, t.second)) + ".png", img)


camera.release()
del(camera)


