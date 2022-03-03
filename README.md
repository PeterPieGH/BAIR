# BAIR
BAIR - Biological Affordable Imaging with Raspberry Pi

Installing and Running the Imaging Software: 

Open the Command Line on your Raspberry Pi

Type cd /home/pi/your/destination/folder/ 

To clone (i.e. download) the BAIR git repository type git clone https://github.com/PeterPieGH/BAIR.git 

Alternatively, download the python script manually from https://github.com/PeterPieGH/BAIR.git into your destination folder 

Type cd BAIR to change into the folder with the python script 

Type python3 bair_app.py to start the GUI 

Set your interval time by typing in a number then pressing enter on your keyboard (time between taking an image) 

Set your total time by typing in a number then pressing enter on your keyboard (total amount of time you want the time lapse to run) 

If desired, set your ISO and Shutter Speed manually 

If desired set your preferred Image Resolution (the maximum setting will vary depending on the type of camera you use) 

Set the directory you want the images to be saved in (note: do not try and save to an external hard drive or flash drive directly from the GUI) 

Set your preferred filename prefix 

Click show preview to ensure your camera is focused on the subject 

Click Take Snapshot to take a single still image 

If video is checked BAIR will automatically create a timelapse video using the images it takes at the end of the total time; the longer the total time the longer it will take to create the video (note: do not close the BAIR gui while the video is processing or it will corrupt the video file) 

Click Start to begin your timelapse! 
