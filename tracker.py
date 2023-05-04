#!/usr/bin/python
# -*- coding: utf-8 -*-
# move a servo from a Tk slider - scruss 2012-10-28
 
import pyfirmata
import time
import sounddevice as sd
import soundfile as sf
# don't forget to change the serial port to suit
board = pyfirmata.Arduino('COM5')
 
# start an iterator thread so
# serial buffer doesn't overflow

filename = 'lock.wav'
        # Extract data and sampling rate from file
data, fs = sf.read("lock.wav", dtype='float32')
# set up pin D9 as Servo Output
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin11 = board.get_pin("d:11:s")
pin13 = board.get_pin('d:13:o')
 
pin9.write(90)
pin10.write(90)
pin11.write(180 - 44)



def fire(sound=False):
        print("firing")
        
        pin11.write(180 - 66)
        
        time.sleep(.2)
        
        pin11.write(180 - 44)
        
        if sound:
                
                sd.play(data, fs, device=6)
                status = sd.wait()  # Wait until file is done playing
        time.sleep(.2)
       

        

# set up GUI

def laserOn():
        pin13.write(1)
def laserOff():
        pin13.write(0)
# draw a nice big slider for servo position

def laserFunc(cx, cy):
        
        serx = int(cx)
        sery = int(cy)
        pin9.write(serx)
        pin10.write(sery)

y_max = 48
y_min = 85
x_max = 0
x_min = 0

#84 62