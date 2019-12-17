import numpy as np
import cv2
import keras
from keras.models import load_model
from pynput.keyboard import Key, Listener
import time
from time import sleep
from serial import Serial

arduino = Serial('/dev/ttyACM0', 9600, timeout=0)
time.sleep(2)
model = load_model('/home/dhruv_d/Desktop/CNN_SGD.h5')
vcap = cv2.VideoCapture('http://192.168.1.110:8080/video')
commands = {0: 'forward', 1: 'left', 2: 'right', 3: 'stop'}

fps = 0.6
framerate = 0.50

# Made in collaboration (<3) with Shaun Fernandes (github.com/shaunferns26)
# Car goes forward, then shifts to reverse gear for a split second which acts as a break
# Car takes aprox 0.75 seconds from the time it starts till the time it stops
#
# T = 0 ms :
#       Read image
# ... :
#       Image begins being processed by CNN
# T =~ 070 ms :
#       MLP completes processing, return direction to turn
#       Car begins to move in direction specified
# T =~ 820 ms :
#       Car stops moving
# (This is when a new image should be read. Loop back to T = 0 ms.)
# (This total time is what the 'framerate' should be set to)
#
#
# Since an image is needed for the MLP, the MLP's returned direction is needed for movement
#   and movement must end before getting the next image, none of these can be run in parallel.
#   Hence, there will always be a delay of 1.07 seconds between 2 loop iterations,
#   and atleast 0.07 second delay where the car is not moving (but the CPU is processing)
#
# All you need to do is confirm each of these:
#   1) Time taken to capture image = 9.5 x 10^-7 s
#   2) Time taken to predict model = 0.0311 s
#   3) Time taken to execute drive comand = 0.40 s
#   4) Time the car takes to come to a complete halt after it has started moving = 0.17s
#
# The first 3 should be printed on the screen each iteration, so just set each of
# them to what seems to be their average time taken.
#
# The last one You will have to whip out your stopwatch and measure manually, from
# the time the car starts till the time it has completely stopped moving (should be around 0.7/0.8 sec).
# (set framerate to 2 so you have a good amount of gap between each iteration to measure).
#
# Once you have all these 4 values, just add them up and you get what is your ideal 'framerate'.
# Maybe add 0.1 or 0.2 seconds extra to be on the safe side while still having minimal delay.
# And once that's done, remove all lines relating to time from within the loop.


def direction(prediction):
    if prediction == 0:
        arduino.write(b'w')
        sleep(0.25)
        arduino.write(b's')
        sleep(0.15)
        arduino.write(b'q')

    if prediction == 1:
        arduino.write(b'a')
        arduino.write(b'w')
        sleep(0.25)
        arduino.write(b's')
        sleep(0.15)
        arduino.write(b'f')

    if prediction == 2:
        arduino.write(b'd')
        arduino.write(b'w')
        sleep(0.25)
        arduino.write(b's')
        sleep(0.15)
        arduino.write(b'f')

    if prediction == 3:
        arduino.write(b'f')


def drive():
    vcap = cv2.VideoCapture('http://192.168.1.110:8080/video')

    timeOld = time.time()
    while True:
        if(time.time() - timeOld > framerate):
            print("time taken by last loop: ", time.time()-timeOld)
            timeOld = time.time()
            time1 = time.time()
            print("capturing image at: ", time.time()-time1)
            vcap = cv2.VideoCapture('http://192.168.1.110:8080/video')
            ret, frame = vcap.read()
            cv2.imshow('AutoPilot', frame)
            img = np.asarray(frame, dtype='float32')
            # img = np.asarray((frame.content), dtype='float32')
            img = img[110:, :, :]
            img /= 255
            img = np.expand_dims(img, axis=0)
            time2 = time.time()
            print("time taken to capture image: ", time2 - time1)
            pred = model.predict_classes(img)
            time3 = time.time()
            print("time taken to predict model: ", time3 - time2)
            print(commands[pred[0]])
            direction(pred)
            print("time taken to execute drive command: ", time.time() - time3)
        else:
            vcap.grab()
        if(cv2.waitKey(22) and 0xFF == 27):
            break
            cv2.destroyAllWindows()


drive()
