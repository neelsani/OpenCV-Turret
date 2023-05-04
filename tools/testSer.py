#!/usr/bin/python
# -*- coding: utf-8 -*-
# move a servo from a Tk slider - scruss 2012-10-28
 
import pyfirmata
from tkinter import *

# don't forget to change the serial port to suit
board = pyfirmata.Arduino('COM7')
 
# start an iterator thread so
# serial buffer doesn't overflow

 
# set up pin D9 as Servo Output
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin11 = board.get_pin("d:11:s")
pin13 = board.get_pin('d:13:o')
 
pin9.write(90)
pin10.write(90)
pin11.write(180 - 44)
def move_servo(a):
    pin9.write(a)

def move_servob(a):
    pin10.write(a)
def motion(event):
        x, y = event.x, event.y
        #print("event")
        serx = int(x/7.111111)
        sery = int(y/4)
        print(str(serx) + " , " + str(sery))
        move_servo(serx)
        move_servob(sery)


# set up GUI
root = Tk()
def laser():
        if var1.get() == 1:
                pin13.write(1)
        else:
                pin13.write(0)
# draw a nice big slider for servo position

var1 = IntVar()
c1 = Checkbutton(root, text='Python',variable=var1, onvalue=1, offvalue=0, command=laser)
c1.pack()
# run Tk event loop
root.bind('<Motion>', motion)
root.geometry("1280x720")
root.mainloop()

#top left : 39 41
#top right: 138 40
#bottom right 130 86
#bottom left 44 84