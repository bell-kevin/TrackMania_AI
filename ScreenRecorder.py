# Records gameplay
# s - starts recording
# f - finishes recording
# x - same as f, but cancels (no shots will be saved)
# q - quits recorder
#
# python ScreenRecorder.py first_person width height

from PIL import Image
import numpy as np
import keyboard
import pathlib
import sys
import socket
from struct import unpack
import GetData
import threading
from Screenshot import screenshot

if len(sys.argv) < 4:
    print('Not enough arguments.')
    exit()

driver_camera = sys.argv[1]

def data_getter_function():
    global data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 9000))
        while True:
            data = GetData.get_data(s)


data_getter_thread = threading.Thread(target=data_getter_function, daemon=True)
data_getter_thread.start()

# old recorder

logfile = './log.txt'

if pathlib.Path(logfile).exists():
    file = open(logfile, 'r')
    log = int(file.read()) + 1
    file.close()
else:
    log = 0


#img = ImageGrab.grab()

# rldu

frame_width = int(sys.argv[2]) 
frame_height = int(sys.argv[3])
print(frame_width)
print(frame_height) 

x = 0

image_dir = './images/' + driver_camera + '/'

pathlib.Path(image_dir + '0000').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0001').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0010').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0011').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0100').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0101').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0110').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '0111').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1000').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1001').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1010').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1011').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1100').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1101').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1110').mkdir(parents=True, exist_ok=True)
pathlib.Path(image_dir + '1111').mkdir(parents=True, exist_ok=True)

clear_list = []

while not keyboard.is_pressed('q'):
    if not keyboard.is_pressed('s'):
        continue

    temp_stint = []  
    while True:
        x = x+1

        speed = data['speed']
        
        frame = Image.fromarray(screenshot(w=frame_width, h=frame_height))

        up = int(keyboard.is_pressed('up'))
        down = int(keyboard.is_pressed('down'))
        left = int(keyboard.is_pressed('left'))
        right = int(keyboard.is_pressed('right'))

        image = image_dir + str(up+down*10+left*100+right*1000+10000)[1:] + '/' + \
            str(log) + '_' + str(x) + '_' + str(int(speed)) + '.jpg'
        
        temp_stint.append(image)
        
        frame.save(image)
        print(image)

        if keyboard.is_pressed('x'):
            clear_list.append(temp_stint)
            break

        if keyboard.is_pressed('f'):
            break

for stint in clear_list:
    for image in stint:
        pathlib.Path(image).unlink()

file = open(logfile, 'w')
file.write(str(log))
file.close()
