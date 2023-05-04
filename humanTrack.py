import cv2
import numpy as np
from cvzone import FPS
from personEngine import personTrack
from tracker import laserFunc, laserOff, laserOn, fire
import threading
import time
import math
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
fireThread = threading.Thread(target=fire, name="shooter")
fps = FPS()
pT = personTrack()
capx = 1280
capy = 720
cenX = capx/2
cenY = capy/2
cap = cv2.VideoCapture(0)
theTime = 0
deltaTime = 0
cap.set(3,capx)
cap.set(4,capy)
avail = None
positionX = 90
positionY = 90
maxAdjFactorX = 7.5
maxAdjFactorY = maxAdjFactorX


def adjustPos(cx, cy, adjSize=0):
	global positionX
	global positionY
	global cenX
	global cenY
	percentX = ((abs(cx-cenX))/cenX)
	percentY = ((abs(cy-cenY))/cenY)/1.618
	percentXpid = 0
	percentYpid = 0
	propX = maxAdjFactorX * percentX
	propY = maxAdjFactorY * percentY	
	#print("propX: " + str(propX))
	#print("propY: " + str(propY))
	if cx < cenX - adjSize:
			positionX += propX
			if positionX > 180:
				positionX = 180
			else:
				positionX = positionX 
		
	elif cx > cenX + adjSize:
		positionX -= propX
		if positionX < 1:
			positionX = 1
		else: 
			positionX = positionX

	if cy < cenY - adjSize:
		positionY += propY
		if positionY > 145:
			positionY = 145
		else:
			positionY = positionY 
	
	elif cy > cenY + adjSize:
		positionY -= propY
		if positionY < 57:
			positionY = 57
		else: 
			positionY = positionY
	#print("posX: " + str(positionX))
	#print("posY: " + str(positionY))		
		
	laserFunc(180 - positionX, 180 - positionY)


def drawThings(frame, x1, y1, x2, y2, cx, cy, deltaTime, trace=False):
	if fireThread.is_alive() == True:

		cv2.putText(frame,"Firing", (1000 ,70), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255))
		cv2.putText(frame,str(round(deltaTime,1)), (0 ,710), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255))
		cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 5)
	else:
		cv2.putText(frame,str(round(deltaTime,1)), (0 ,710), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0))
		cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)
	#cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)
	cv2.circle(frame, (cx, cy), 5, (255,0,255), -1)
	cv2.circle(frame, (x2,y2), 8, (255,0,255), -1)
	cv2.circle(frame, (x1,y1), 8, (0,255,0), -1)
	loc = "centroid: " + str(cx) + ", " + str(cy)
	cv2.putText(frame,loc,(cx+10,cy-10), cv2.FONT_HERSHEY_DUPLEX, .45, (234,46,128))
	#cv2.putText(frame,str(deltaTime), (0 ,710), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
	

def shootDaBih(frame, trStatus):
	global theTime
	global fireThread
	
	if theTime == 0 and trStatus:
		#print("tracking")
		theTime = time.time() 
	if not trStatus:
		theTime = 0
	deltaTime = time.time() - theTime
	if deltaTime >= 6 and trStatus:
		print(deltaTime)
		theTime = 0
		if fireThread.is_alive() == False:
			fireThread = threading.Thread(target=fire, name="shooter")
			fireThread.start()
	return deltaTime
while True:
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)


	x1, y1, x2, y2, cx, cy, head = pT.findPerson(frame)




	if x1:
		
		x1 = head[0]
		y1 = head[1]
		x2 = head[2]
		y2 = head[3]
		cx = head[4]
		cy = head[5]
		
		trStatus = x2 < cenX < x1 and y2<cenY<y1
		#print(trStatus)
		#print("1", x1,y1)
		#print(x2,y2)
		adjustPos(cx,cy)
		deltaTime = shootDaBih(frame, trStatus)

		drawThings(frame,x1,y1,x2,y2,cx,cy, deltaTime,trace=False)
	else:
		#print("resetting")
		theTime = 0
	fps.update(img=frame)
	cv2.imshow("yolo", frame)
	k = cv2.waitKey(1)

	if k & 0xFF == ord('l'):
		laserOn()
	elif k & 0xFF == ord('o'):
		laserOff()
	elif k & 0xFF == ord('r'):
		positionX =90
		positionY = 90
		laserFunc(positionX,positionY)
		time.sleep(.5)
	elif k & 0xFF == ord('f'):
		print(fireThread.is_alive())
		if fireThread.is_alive() == False:
			fireThread = threading.Thread(target=fire, name="shooter")
			fireThread.start()
	elif k & 0xFF == ord('q'):
		laserOff()
		laserFunc(90,90)
		break
	
	#sock.sendto(str.encode(str(str(positionX)+","+str(positionY))), serverAddressPort)   FOR UNITY 
cap.release()
cv2.destroyAllWindows()