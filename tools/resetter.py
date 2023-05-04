import pyfirmata


# don't forget to change the serial port to suit
board = pyfirmata.Arduino('COM7')
 
# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
 
# set up pin D9 as Servo Output
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin13 = board.get_pin('d:13:o')


pin10.write(90)
pin9.write(90)