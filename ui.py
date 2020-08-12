

import os, shutil
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import tovid

root = tk.Tk()

# Create the frames
frame_args = dict(padx=5, pady=5)
frame_config = tk.Frame(root)#, bg="green")
frame_lastfr = tk.Frame(root, bg="blue")
frame_bottom = tk.Frame(root)#, bg="red")

frame_config.grid(row=0, column=0, sticky=tk.S+tk.W+tk.N, rowspan=2, **frame_args)
frame_lastfr.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E, **frame_args)
frame_bottom.grid(row=1, column=1, sticky=tk.S+tk.W+tk.E, **frame_args)

# Canvas
cnv_lastfr = tk.Canvas(frame_lastfr, width=800, height=600)
cnv_lastfr.pack(fill=tk.BOTH, expand=True)

#img_lastfr = tk.PhotoImage(file='4.PNG')
#cnv_lastfr.create_image(0, 0, image=img_lastfr, anchor=tk.NW)

### Configuration
lbl_config = ttk.Label(frame_config, text="Configuration")
lbl_config.pack(pady=10)

ttk.Separator(frame_config, orient=tk.HORIZONTAL).pack(pady=20, fill=tk.BOTH)

# Snap period
lbl_period = ttk.Label(frame_config, text="Take frame each seconds =")
var_period = tk.IntVar()
sbx_period = ttk.Spinbox(frame_config, from_=1, to=3600, textvariable=var_period)
var_period.set(10)
lbl_period.pack()
sbx_period.pack()

ttk.Separator(frame_config, orient=tk.HORIZONTAL).pack(pady=20, fill=tk.BOTH)

"""# Keep n days
var_keepn = tk.IntVar()
sbx_keepn = ttk.Spinbox(frame_config, state="disabled", from_=1, textvariable=var_keepn)
var_keepn.set(1)
def on_ckb_keepn():
    sbx_keepn.configure(state="enabled" if "selected" in ckb_keepn.state() else "disabled")
ckb_keepn = ttk.Checkbutton(frame_config, text="Delete folder each days =", command=on_ckb_keepn)
for _ in range(2):ckb_keepn.invoke()
ckb_keepn.pack()
sbx_keepn.pack()

ttk.Separator(frame_config, orient=tk.HORIZONTAL).pack(pady=20, fill=tk.BOTH)"""

# Save vid each h hour
var_savevid_h = tk.IntVar()
sbx_savevid = ttk.Spinbox(frame_config, state="enabled", from_=1, to=168, textvariable=var_savevid_h)
var_savevid_h.set(0)

var_savevid_fps = tk.IntVar()
sbx_savevid_fps = ttk.Spinbox(frame_config, state="enabled", from_=1, to=168, textvariable=var_savevid_fps)
var_savevid_fps.set(30)

lbl_savevid_fps = ttk.Label(frame_config, text="FPS =")

def on_ckb_savevid():
    sbx_savevid.configure(state="enabled" if "selected" in ckb_savevid.state() else "disabled")
    ckb_savevid_delframes.configure(state="enabled" if "selected" in ckb_savevid.state() else "disabled")
ckb_savevid = ttk.Checkbutton(frame_config, text="Make avi when hour =", command=on_ckb_savevid)
ckb_savevid_delframes = ttk.Checkbutton(frame_config, text="Delete images afterwards")
ckb_savevid.invoke()
ckb_savevid_delframes.invoke()
ckb_savevid.pack()
sbx_savevid.pack()
lbl_savevid_fps.pack()
sbx_savevid_fps.pack()
ckb_savevid_delframes.pack()


### Bottom bar
lbl_folder = ttk.Label(frame_bottom, text="Current save location:", compound=tk.CENTER)
lbl_folder.pack(side=tk.LEFT, anchor=tk.W, padx=5)

ety_daydirpath = ttk.Entry(frame_bottom, text="test")
ety_daydirpath.delete(0, tk.END)
ety_daydirpath.insert(0, os.path.dirname(os.path.realpath(__file__)))
ety_daydirpath.configure(state="readonly")
ety_daydirpath.pack(side=tk.LEFT, anchor=tk.W, padx=5, fill=tk.X, expand=True)

lbl_filename = ttk.Label(frame_bottom, text="PLACEHOLDER", compound=tk.CENTER)
lbl_filename.pack(side=tk.LEFT, anchor=tk.W)

def on_btn_change_daydirpath():
    folder_selected = filedialog.askdirectory()
    ety_daydirpath.config(state="")
    ety_daydirpath.delete(0,tk.END)
    ety_daydirpath.insert(0, folder_selected)
    ety_daydirpath.config(state="readonly")
    
btn_change_daydirpath = ttk.Button(frame_bottom, text="Browse...", command=on_btn_change_daydirpath)
btn_change_daydirpath.pack(side=tk.LEFT, anchor=tk.W, padx=20)

lbl_lastts = ttk.Label(frame_bottom, text="Last frame: -", compound=tk.CENTER)
lbl_lastts.pack(side=tk.LEFT, anchor=tk.E)

# grid config
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

#root.configure(background='black')

import datetime
from pathlib import Path
import cv2

class Backend:
    refresh_freq = 1/30

    def __init__(self):
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(0)
        
        width  = self.camera.get(3) # float
        height = self.camera.get(4) # float
        print("Camera", self.camera, "at res", width, "*", height)

        cnv_lastfr.config(width=width, height=height)

        self.curr_d = None        
        self.curr_folder = None
        self.last_ts = None
        

    def on_closing(self):
        root.destroy()
        self.camera.release()
        del(self.camera)
        cv2.destroyAllWindows()
        print("done.")

    def refresh_save_folder(self):
        self.curr_folder = ety_daydirpath.get() + "/"+'_'.join(str(_) for _ in self.curr_d)
        lbl_filename["text"] = '/' + self.curr_folder.split('/')[-1]
        Path(self.curr_folder).mkdir(parents=True, exist_ok=True)

    def update(self):
        
        t = datetime.datetime.now()

        if self.curr_d != (t.year, t.month, t.day):
            self.curr_d = (t.year, t.month, t.day)
            print("Changed day to", self.curr_d)
        
        self.refresh_save_folder()

        _, self.last_img_arr = self.camera.read()
        t = datetime.datetime.now()
        period = var_period.get()
        if t.second %  (period if 0 < period <= 3600 else 30) == 0 and (not self.last_ts or self.last_ts.second != t.second):

            if "selected" in ckb_savevid.state() and t.second == 0 and t.minute == 0 and t.hour == int(var_savevid_h.get()):
                vid_fpath = '_'.join(str(x) for x in self.curr_d) + "_vid.avi"
                print("Saving video as:", vid_fpath)
                tovid.video_from(self.curr_folder, vid_fpath, var_savevid_fps.get())
                if "selected" in ckb_savevid_delframes.state():
                    shutil.rmtree(self.curr_folder)

            fpath = self.curr_folder + '/' + '_'.join(str(_) for _ in (t.hour, t.minute, t.second)) + ".png"
            lbl_lastts["text"] = "Last frame: " + fpath.split('/')[-1]
            cv2.imwrite(fpath, self.last_img_arr)

            self.last_img = ImageTk.PhotoImage(image=Image.fromarray(self.last_img_arr[..., [2, 1, 0]]))
            cnv_lastfr.create_image(0, 0, image=self.last_img, anchor=tk.NW)
            self.last_ts = t


        root.after(int(1 / Backend.refresh_freq), self.update)

be = Backend()
root.protocol("WM_DELETE_WINDOW", be.on_closing)
root.after(int(1 / Backend.refresh_freq), be.update)
root.mainloop()
