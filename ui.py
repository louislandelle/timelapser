

import os, shutil
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import util

root = tk.Tk()

# Create the frames
frame_args = dict(padx=5, pady=5)
frame_config = tk.Frame(root)#, bg="green")
frame_lastfr = tk.Frame(root)#, bg="blue")
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
lbl_config = ttk.Label(frame_config, text="Configuration", font="bold")
lbl_config.pack(pady=10)

# Camera resolution
lbl_camres = ttk.Label(frame_config, text="Camera resolution")
var_camres = tk.StringVar()
cbb_camres = ttk.Combobox(frame_config, textvariable=var_camres, state="readonly")

btn_fetch = ttk.Button(frame_config, text="Scan available (up to 1080p)")

lbl_custom = ttk.Label(frame_config, text="Custom resolution")

def custom_wh_frame():
    fr = tk.Frame(frame_config)

    var_custw, var_custh = tk.IntVar(), tk.IntVar()

    lbl_w = ttk.Label(fr, text="Width:")
    lbl_h = ttk.Label(fr, text="Height:")
    sbx_custw = ttk.Spinbox(fr, textvariable=var_custw, width=8)
    sbx_custh = ttk.Spinbox(fr, textvariable=var_custh, width=8)
    btn_set = ttk.Button(fr, text="Set")
    custom_wh_frame.btn_set = btn_set
    custom_wh_frame.var_custw = var_custw
    custom_wh_frame.var_custh = var_custh

    lbl_w.grid(row=0, column=0)
    sbx_custw.grid(row=0, column=1)
    lbl_h.grid(row=1, column=0)
    sbx_custh.grid(row=1, column=1)
    btn_set.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S)
    return fr

lbl_camres.pack(pady=10)
cbb_camres.pack()
btn_fetch.pack()
lbl_custom.pack()
custom_wh_frame().pack()
ttk.Separator(frame_config, orient=tk.HORIZONTAL).pack(pady=20, fill=tk.BOTH)

# Saved images format
lbl_imgfmt = ttk.Label(frame_config, text="Frame compression")
var_imgfmt = tk.StringVar()
cbb_imgfmt = ttk.Combobox(frame_config, textvariable=var_imgfmt, state="readonly")
cbb_imgfmt['values'] = ("PNG", "JPEG (quality 50) - default", "JPEG (quality 95)", "JPEG (quality 100)")
cbb_imgfmt.current(1)
lbl_imgfmt.pack(pady=10)
cbb_imgfmt.pack()

ttk.Separator(frame_config, orient=tk.HORIZONTAL).pack(pady=20, fill=tk.BOTH)

# Video saved format
#TODO?

# Snap period
lbl_period = ttk.Label(frame_config, text="Frame snapshot period (s)")
var_period = tk.IntVar()
sbx_period = ttk.Spinbox(frame_config, from_=1, to=3600, textvariable=var_period)
var_period.set(10)
lbl_period.pack(pady=10)
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

lbl_savevid_fps = ttk.Label(frame_config, text="Frames-per-second")

btn_savevid_now = ttk.Button(frame_config, text="Save video now")

def on_ckb_savevid():
    sbx_savevid.configure(state="enabled" if "selected" in ckb_savevid.state() else "disabled")

ckb_savevid = ttk.Checkbutton(frame_config, text="Save video at (h, of 24)", command=on_ckb_savevid)
ckb_savevid_delframes = ttk.Checkbutton(frame_config, text="Delete images afterwards")
ckb_savevid.invoke()
ckb_savevid_delframes.invoke()
ckb_savevid.pack()
sbx_savevid.pack()
btn_savevid_now.pack()
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
    if folder_selected:        
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

        width  = int(self.camera.get(3)) # float
        height = int(self.camera.get(4)) # float
        print("Camera", self.camera, "at res", width, "*", height)
        self.default_res = (width, height)
        self.default_res_str = str(width) + "x" + str(height) + " - default"
        cbb_camres["values"] = [self.default_res_str,]
        cbb_camres.current(0)

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

    def save_video(self):
        vid_fpath = '_'.join(str(x) for x in self.curr_d) + "_vid.avi"
        print("Saving video as:", vid_fpath)
        util.video_from(self.curr_folder, vid_fpath, var_savevid_fps.get())
        if "selected" in ckb_savevid_delframes.state():
            shutil.rmtree(self.curr_folder)

    def set_resolution_closest(self, w, h):
        if not w > 0: w = 1
        if not h > 0: h = 1
        self.set_resolution_exact(w, h)
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if width != w or height != h:
            messagebox.showwarning("Unsupported resolution", "Custom resolution is not supported. Set to closest available:" + str(width) + "x" + str(height))
    
    def set_resolution_exact(self, w, h):
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    def fetch_cam_res(self):
        # Fetch available camera resolutions and add them to drop-down options
        messagebox.showinfo("Info", "This operation might take a few seconds.")
        available_res = util.fetch_cam_res()
        messagebox.showinfo("Info", "Added available resolutions (up to 1080p) to drop-down options.")
        cbb_camres["values"] = [self.default_res_str,] + [str(x) + "x" + str(y) for (x, y) in available_res if not (x, y) == self.default_res]

    def update(self):
        
        t = datetime.datetime.now()

        if self.curr_d != (t.year, t.month, t.day):
            self.curr_d = (t.year, t.month, t.day)
            print("Changed day to", self.curr_d)
        
        self.refresh_save_folder()

        _, self.last_img_arr = self.camera.read()
        if self.last_img_arr is None:
            # Could not fetch image from webcam
            root.after(int(1 / Backend.refresh_freq), self.update)
            return

        t = datetime.datetime.now()
        period = var_period.get()
        if t.second %  (period if 0 < period <= 3600 else 30) == 0 and (not self.last_ts or self.last_ts.second != t.second):

            if "selected" in ckb_savevid.state() and t.second == 0 and t.minute == 0 and t.hour == int(var_savevid_h.get()):
                self.save_video()

            # Fetch compression paramters
            use_jpeg = not (cbb_imgfmt.get() == "PNG")
            jpeg_quality = int(cbb_imgfmt.get().split("quality ")[1].split(")")[0]) if use_jpeg else None

            # Compute path for next frame and save it using compression parameters
            fpath = self.curr_folder + '/' + '_'.join(str(_) for _ in (t.hour, t.minute, t.second)) + (".png" if not use_jpeg else ".jpeg")
            lbl_lastts["text"] = "Last frame: " + fpath.split('/')[-1]
            cv2.imwrite(fpath, self.last_img_arr, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality] if use_jpeg else [])

            # Load last frame and display it on canvas
            self.last_img = ImageTk.PhotoImage(image=Image.fromarray(self.last_img_arr[..., [2, 1, 0]]))
            cnv_lastfr.create_image(0, 0, image=self.last_img, anchor=tk.NW)
            self.last_ts = t

        root.after(int(1 / Backend.refresh_freq), self.update)

be = Backend()

# Link front-end buttons to back-end commands
btn_savevid_now.config(command=be.save_video)
custom_wh_frame.btn_set.config(command=lambda: be.set_resolution_closest(
    custom_wh_frame.var_custw.get(),
    custom_wh_frame.var_custh.get()))
btn_fetch.config(command=be.fetch_cam_res)

# Link front-end var changes to back-end commands

var_camres.trace('w', lambda *a: be.set_resolution_exact(
    *[int(x if not "default" in x else x.split(" ")[0]) for x in var_camres.get().split("x")]
))


# Run mainloop
root.protocol("WM_DELETE_WINDOW", be.on_closing)
root.after(int(1 / Backend.refresh_freq), be.update)
root.title("Timelapser")
root.mainloop()
