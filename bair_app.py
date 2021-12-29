#! /usr/bin/python3

# BAIR - Biological Affordable Imaging with Raspberry Pi
# Version 1.0.0
# Date 12/29/2021
# Developed by: Peter Pietrzyk

# This software was developed and tested in Python 3.7.3  

import os
import time
from fractions import Fraction
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import ACTIVE, DISABLED
from picamera import PiCamera
import picamera.array

class BairApp:

    def __init__(self):

        self.master = tk.Tk()
        self.master.title('BAIR - Biological Affordable Imaging with Raspberry Pi')
        self.master['padx'] = 5
        self.master['pady'] = 5


        """ Initialize variables """
        self.is_running = None                  # None if timelapse is not running

        # Intervalometer variables
        self.hour_interval_var = tk.IntVar()    # Hour value for interval duration
        self.min_interval_var = tk.IntVar()     # Minute value for interval duration
        self.sec_interval_var = tk.IntVar()
        self.hour_ttime_var = tk.IntVar()
        self.min_ttime_var = tk.IntVar()
        self.sec_ttime_var = tk.IntVar()
        self.num_entry = tk.StringVar()

        # Camera options
        self.iso_options = [100, 200, 320, 400, 500, 640, 800]
        self.shutter_speed_options = ["1", "1/2", "1/4", "1/8", "1/15", "1/30", "1/60", "1/125", "1/250", "1/500", "1/1000"]
        self.resolution_options = ["2592 x 1944", "1296 x 972", "1296 x 730", "640 x 480", "1920 x 1080"]

        # Camera settings
        self.var_auto_iso = tk.IntVar(value=1)
        self.iso_var = tk.IntVar(value=self.iso_options[0])
        self.var_auto_shutter = tk.IntVar(value=1)
        self.speed_var = tk.StringVar(value=self.shutter_speed_options[7])
        self.resolution_var = tk.StringVar(value=self.resolution_options[1])

        # Path variables
        self.pathEntry = tk.StringVar()
        self.prefix_var = tk.StringVar(value="image_")

        # Video variables
        self.var_video = tk.IntVar(value=1)


        """ Initialize Camera """
        self.camera = PiCamera()
        self.set_image_res(self.resolution_var.get())
        self.set_shutter(self.speed_var.get())
        self.set_iso(self.iso_var.get())


        """ Timelapse """
        # Frame for timelapse settings
        timelapseFrame = tk.LabelFrame(self.master, text="Interval Settings", padx=5, pady=5)
        timelapseFrame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        # Create Headers
        header_interval = tk.Label(timelapseFrame, text="Interval time")
        header_interval.grid(row=0,column=1,padx=5)

        header_tottime = tk.Label(timelapseFrame, text="Total time")
        header_tottime.grid(row=0,column=3,padx=5)

        label_num = tk.Label(timelapseFrame, text="Image number:")        
        label_num.grid(row=0,column=4,padx=5)

        # Create and place interval labels
        label_hours = tk.Label(timelapseFrame, text="Hours:")
        label_hours.grid(row=1,column=0, sticky=tk.E, padx=5)

        label_minutes = tk.Label(timelapseFrame, text="Minutes:")
        label_minutes.grid(row=2,column=0, sticky=tk.E, padx=5)

        label_seconds = tk.Label(timelapseFrame, text="Seconds:")
        label_seconds.grid(row=3,column=0, sticky=tk.E, padx=5)        

        # Create and place interval buttons
        hour_interval_button = tk.Spinbox(timelapseFrame, textvariable=self.hour_interval_var, from_=0, to=999, command=self.set_interval, width=5)
        hour_interval_button.grid(row=1,column=1, padx=5)

        min_interval_button = tk.Spinbox(timelapseFrame, textvariable=self.min_interval_var, from_=0, to=59, command=self.set_interval, width=5)
        min_interval_button.grid(row=2,column=1, padx=5)

        sec_interval_button = tk.Spinbox(timelapseFrame, textvariable=self.sec_interval_var, from_=0, to=59, command=self.set_interval, width=5)
        sec_interval_button.grid(row=3,column=1, padx=5)

        # Create and place time labels
        label_hours = tk.Label(timelapseFrame, text="Hours:")
        label_hours.grid(row=1,column=2, sticky=tk.E, padx=5)

        label_minutes = tk.Label(timelapseFrame, text="Minutes:")
        label_minutes.grid(row=2,column=2, sticky=tk.E, padx=5)

        label_seconds = tk.Label(timelapseFrame, text="Seconds:")
        label_seconds.grid(row=3,column=2, sticky=tk.E, padx=5)

        # Create and place time buttons
        hour_ttime_button = tk.Spinbox(timelapseFrame, textvariable=self.hour_ttime_var, from_=0, to=999, command=self.set_interval, width=5)
        hour_ttime_button.grid(row=1,column=3, padx=5)

        min_ttime_button = tk.Spinbox(timelapseFrame, textvariable=self.min_ttime_var, from_=0, to=59, command=self.set_interval, width=5)
        min_ttime_button.grid(row=2,column=3, padx=5)

        sec_ttime_button = tk.Spinbox(timelapseFrame, textvariable=self.sec_ttime_var, from_=0, to=59, command=self.set_interval, width=5)
        sec_ttime_button.grid(row=3,column=3, padx=5)

        # Create and place image number entry
        num_images_botton =  tk.Entry(timelapseFrame, textvariable=self.num_entry, width=6)
        num_images_botton.grid(row=1,column=4, padx=5)
        num_images_botton.bind('<Return>', self.set_total_time)


        """ Camera Setting """
        camSettingsFrame = tk.LabelFrame(self.master, text="Camera Settings", padx=5, pady=5)
        camSettingsFrame.grid(row=1, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        # ISO
        label_iso = tk.Label(camSettingsFrame, text="ISO:")
        label_iso.grid(row=0,column=0, sticky=tk.E, padx=5)

        auto_iso = tk.Checkbutton(camSettingsFrame, variable=self.var_auto_iso, text="auto", command=self.set_iso_auto)
        auto_iso.grid(row=0,column=1, padx=5)

        self.iso_menu = tk.OptionMenu(camSettingsFrame, self.iso_var, *self.iso_options, command=self.set_iso)
        self.iso_menu.configure(width=6)
        self.iso_menu.configure(state="disabled")
        self.iso_menu.grid(row=0,column=2, padx=5)

        # Shutter speed
        label_shutter = tk.Label(camSettingsFrame, text="Shutter Speed:")
        label_shutter.grid(row=1,column=0, sticky=tk.E, padx=5)

        auto_shutter = tk.Checkbutton(camSettingsFrame, variable=self.var_auto_shutter, text="auto", command=self.set_shutter_auto)
        auto_shutter.grid(row=1,column=1, padx=5)
        
        self.speed_menu = tk.OptionMenu(camSettingsFrame, self.speed_var, *self.shutter_speed_options, command=self.set_shutter)
        self.speed_menu.configure(width=6)
        self.speed_menu.configure(state="disabled")
        self.speed_menu.grid(row=1,column=2, padx=5)       
        
        # Image size
        label_resolution = tk.Label(camSettingsFrame, text="Image Resolution:")
        label_resolution.grid(row=0,column=3, sticky=tk.E, padx=5)
        
        resolution_menu = tk.OptionMenu(camSettingsFrame, self.resolution_var, *self.resolution_options, command=self.set_image_res)
        resolution_menu.configure(width=11)
        resolution_menu.grid(row=0,column=4, padx=5)


        """ Folder and file name """
        pathFrame = tk.LabelFrame(self.master, text="Directory", padx=5, pady=5)
        pathFrame.grid(row=2, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        label_prefix = tk.Label(pathFrame, text="Prefix:")
        label_prefix.grid(row=0,column=0, sticky=tk.E, padx=5)

        prefix_entry =  tk.Entry(pathFrame, textvariable=self.prefix_var)
        prefix_entry.grid(row=0,column=1, padx=5)

        folder_button = tk.Button(pathFrame, text="Select folder", command=self.select_folder)
        folder_button.grid(row=0,column=2, padx=5)

        folder_entry = tk.Entry(pathFrame, textvariable = self.pathEntry)
        folder_entry.grid(row=0,column=3, padx=5)
        

        """ Start/Stop buttons """
        buttons_frame = tk.LabelFrame(self.master, text="Process", padx=5, pady=5)
        buttons_frame.grid(row=3, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        
        video_check = tk.Checkbutton(buttons_frame, variable=self.var_video, text="Video")
        video_check.grid(row=0,column=0, padx=5)

        start_timelapse_button = tk.Button(buttons_frame, text="Start", command=self.start_timelapse)
        start_timelapse_button.grid(row=0,column=1, padx=5)

        stop_timelapse_button = tk.Button(buttons_frame, text="Stop", command=self.stop_timelapse)
        stop_timelapse_button.grid(row=0,column=2, padx=5)

        preview_button = tk.Button(buttons_frame, text="Show Preview", command=self.show_preview)
        preview_button.grid(row=0,column=3, padx=5)

        snapshot_button = tk.Button(buttons_frame, text="Take Snapshot", command=self.take_snapshot)
        snapshot_button.grid(row=0,column=4, padx=5)


    def get_time_interval(self):
        seconds = int(self.sec_interval_var.get())
        minutes = int(self.min_interval_var.get())
        hours = int(self.hour_interval_var.get())
        interval_time = seconds + 60*minutes + 60*60*hours
        return interval_time

    def get_time_total(self):
        seconds = int(self.sec_ttime_var.get())
        minutes = int(self.min_ttime_var.get())
        hours = int(self.hour_ttime_var.get())
        total_time = seconds + 60*minutes + 60*60*hours
        return total_time

    def get_num_images(self):
        try:
            return 1 + int(self.get_time_total() / self.get_time_interval())
        except:
            return 0
    
    def set_interval(self):
        num = self.get_num_images()
        self.num_entry.set(str(num))

    def set_total_time(self, str_entry):
        num = int(self.num_entry.get())
        interval_time = self.get_time_interval()
        
        tot_time = (num-1)*interval_time
        hours, rem = divmod(tot_time,3600)
        minutes, seconds = divmod(rem,60)

        self.sec_ttime_var.set(seconds)
        self.min_ttime_var.set(minutes)
        self.hour_ttime_var.set(hours)

    def set_iso_auto(self):
        if self.var_auto_iso.get() == 0:                # Auto is off
            self.camera.iso = self.iso_var.get()
            self.iso_menu.configure(state=ACTIVE)
        else:                                               # Auto if on
            self.camera.iso = 0
            self.iso_menu.configure(state=DISABLED)

    def set_shutter_auto(self):
        if self.var_auto_shutter.get() == 0:                # Auto is off
            shutter_float = float(Fraction(self.speed_var.get()))
            self.camera.shutter_speed = int(1000000*shutter_float)
            self.speed_menu.configure(state=ACTIVE)
        else:                                               # Auto if on
            self.camera.shutter_speed = 0
            self.speed_menu.configure(state=DISABLED)
    
    def set_iso(self, iso_value):
        if self.var_auto_iso.get() == 0:
            self.camera.iso = iso_value
        else:
            self.camera.iso = 0

    def set_shutter(self, shutter_value):
        if self.var_auto_shutter.get() == 0:
            shutter_float = float(Fraction(shutter_value))
            self.camera.shutter_speed = int(1000000*shutter_float)
        else:
            self.camera.shutter_speed = 0

    def set_image_res(self, img_res):
        x_res, y_res = (int(val) for val in img_res.split('x'))
        self.camera.resolution = (x_res,y_res)
        
    def select_folder(self):
        path = filedialog.askdirectory(title="Select a Folder")
        self.pathEntry.set(path)

    def start_timelapse(self):

        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            
            self.interval_time = self.get_time_interval()
            self.total_time = self.get_time_total()
            self.num_images = self.get_num_images()
            self.counter = 0
            self.timelapse()

    def timelapse(self):
        
        # Take image
        filename = self.prefix_var.get() + '{0:04d}.jpg'.format(self.counter)
        self.camera.capture(os.path.join(self.pathEntry.get(), filename))
        print("Saved " + os.path.join(self.pathEntry.get(), filename))

        self.counter += 1
        if self.counter >= self.num_images: # Finished
            if self.var_video.get():
                self.make_video()
            self.is_running = None
            return

        t_diff = time.time()-self.start_time
        t_wait = self.interval_time - (t_diff % self.interval_time)

        self.is_running = self.master.after(int(1000*t_wait)+1,self.timelapse)


    def make_video(self):
        video_filename = self.prefix_var.get()+"video.mp4"
        #ffmpeg -r 25 -i image_%04d.jpg -g 5 -vcodec libx264 -crf 25 -pix_fmt yuv420p video.mp4
        str_cmd = 'ffmpeg -r 25 -i ' + os.path.join(self.pathEntry.get(),self.prefix_var.get()) + '%04d.jpg -g 5 -vcodec libx264 -crf 25 -pix_fmt yuv420p ' + os.path.join(self.pathEntry.get(),video_filename)
        os.system(str_cmd)
        print("Finished creating video")

    def stop_timelapse(self):
        if self.is_running:
            self.master.after_cancel(self.is_running)
            self.is_running = None
            print("Stopped")

    def show_preview(self):
        self.camera.preview_fullscreen = 'False'
        self.camera.start_preview()
        time.sleep(5)
        self.camera.stop_preview()

    def take_snapshot(self):
        output = picamera.array.PiRGBArray(self.camera)
        self.camera.capture(output, 'rgb')
        image = Image.fromarray(output.array)
        filename_output = filedialog.asksaveasfile(title="Choose a file",filetypes=[('jpeg','*.jpg')])
        image.save(filename_output)


gui = BairApp()
gui.master.mainloop()