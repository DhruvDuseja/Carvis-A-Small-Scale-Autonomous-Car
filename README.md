# Carvis-A-Small-Scale-Autonomous-Car
### Alt-A small-scale rudimentary implementation of a self driving car :red_car:

## The Idea
To make an autonomous car using an Arduino Uno (which _surprisingly_ did not work.)

## The Remake
1. Buy RC car
2. Rewire some components (???)
3. ?????
4. Profit

## The Implementation
The car itself was not modified in any way.
The remote control was modified and connected to the Arduino.

The remote control without the backpanel
![Remote control without backpanel] (/Media/Out_the_box.jpg)

The remote control with the joysticks removed
![Remote control w/o joysticks] (/Media/Out_the_box_wo_stick.jpg)

Wiring from the buttons that would go to the Arduino
![Wiring] (/Media/After_conn.jpg)

## The Way It Works
As mentioned, it was a pretty rudimentary implementation. So, here's how it works.
1. A phone is kept on the back of the car, which streams to a localhost (Check out [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en)).
2. The stream is then accessed directly (with OpenCV), and frames are obtained from it.
3. The frames are preprocessed and passed to a neural network (based on the VGG architecture.)
4. The neural net output is fed into the Arduino, which is hooked onto the remote control, hence controlling the car.

## The Dataset
The path for the car was created by laying out white paper on either side of the car to give it "boundaries".
A piece of paper was kept at the end to symbolise the end of the track.

## Results
![Run 1] (/Media/Video1.gif)

![Run 2] (/Media/Video2.gif)

Two neural networks were trained on the dataset
- VGG Arch : 99.9% accuracy
- MLP : 99.7% accuracy

The car had to be run in steps, as the actual speed was too high, which is why it appears jerk-y.
A delay was also added to allow for frames to be gotten and processed.

### And last but not least, credits to [Shaun Fernandes](https://github.com/shaunferns26)
