""" Program to interfact Arduino with a RC car controller
    and control the car using the arrow keys and Space bar.

    The Car is set to always drive straight, and will turn
    when an arrow key is pressed. It will stop when the
    space bar is held.

    The car is set to go forward for a split and then
    pause for a split (helps reduce speed)

    This part was used to test the Arduino connection and later collect data.

    Credits: Shaun Fernandes (github.com/shaunferns26)
"""

# The arduino program is set to read:
# w - Forward               q - Stop accelerating
# a - Left                  d - Right
# f - Stop all motors       e - Stop turning

################################################################
# you need to uncomment all the "arduino.write(b' ')" lines... #
################################################################

# also the b in the arduino.write is because the arduino only accepts bytes as input, not strings...

import os
import cv2
import uuid
import time
import numpy as np
from time import sleep
from serial import Serial
from threading import Thread
from pynput.keyboard import Key, Listener

arduino = Serial('/dev/ttyACM2', 9600, timeout=0)       # Change the port ('COM5') to the one shown in ardunino IDE
time.sleep(2)                                   # needs 2 seconds to connect to the arduino...


def on_press(key):
    global direction
    global arduino
    if (key in keyPressed) and (not keyPressed[key]):
        print('{0} pressed'.format(key))
        keyPressed[key] = True

        if key == Key.space:
            print("Stopping...")
            direction = 'break'
            arduino.write(b'q')
        elif key == Key.left:
            print("Going Left...")
            direction = 'left'
            arduino.write(b'a')
        elif key == Key.right:
            print("Going Right...")
            direction = 'right'
            arduino.write(b'd')


def on_release(key):
    global direction
    global arduino
    if key == Key.esc:
        return False                            # Stop Key listener

    if key in keyPressed:
        print('{0} release'.format(key))
        keyPressed[key] = False
        print(keyPressed)

        if keyPressed[Key.space]:
            arduino.write(b'q')
            print('q')
            direction = 'break'
        elif keyPressed[Key.left] and (not keyPressed[Key.right]):
            arduino.write(b'a')
            print('a')
            direction = 'left'
        elif keyPressed[Key.right] and (not keyPressed[Key.left]):
            arduino.write(b'd')
            print('d')
            direction = 'right'
        elif (not keyPressed[Key.left]) and (not keyPressed[Key.right]):
            arduino.write(b'e')
            print('e')
            direction = 'forward'


def control():
    oldTime = time.time()
    global arduino
    while True:
        # set the motors to backwards for a short amount of time to simulate a hard brake
        arduino.write(b's')
        sleep(0.05)
        # then stop the motors
        arduino.write(b'q')
        print("pause")
        sleep(pauseDuration)
        # restart motors
        arduino.write(b'w')
        print("resume")
        running = True
        sleep(pauseDuration1)


def imageCapture():
    global direction
    timeOld = time.time()
    path = '/home/dhruv_d/Desktop/npdata'
    while True:
        ret, frame = vcap.read()
        if frame is not None:
            cv2.imshow('frame', frame)
            # print("OpenCV says direction is", direction)
            if (time.time() - timeOld > frameRate):
                data = np.asarray(frame, dtype='float32')
                imgName = '{}_{}'.format(uuid.uuid1(), direction)
                np.save(os.path.join(path, imgName), data)
		#cv2.imwrite(os.path.join(path, imgName), frame)
                oldTime = time.time()
            # Press Esc when focus is on video frame to close the video window
            if cv2.waitKey(22) & 0xFF == 27:
                break
        else:
            print("Frame is None")
            break


vcap = cv2.VideoCapture('http://192.168.1.103:8080/video')
# Dictionary to store which keys are currently being held down
keyPressed = {Key.left: False, Key.right: False, Key.space: False}
# amount of time to stop the car before restarting
# The medium blog dude used 0.10 here, so you may want to change this
pauseDuration = 0.9
pauseDuration1 = 0.22
fps = 10
frameRate = 1/fps
global direction
direction = 'forward'

thread = Thread(target=control, args=())
thread2 = Thread(target=imageCapture, args=())
# These Threads die when main thread dies
thread.daemon = True
thread2.daemon = True
thread.start()
thread2.start()
# thread.join()
# thread2.join()
# Main thread Dies when Listener dies
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
# Listener dies when you press Esc

print("threads finished...exiting")

