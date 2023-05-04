import cvzone
from cvzone.ColorModule import ColorFinder
import cv2 
from collections import deque
import numpy as np
from cvzone import FPS 
import win32api
import win32con
from tracker import laserFunc, laserOff, laserOn, fire
import math
import time 
import threading
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
cap=cv2.VideoCapture(0)


maxAdjFactorX = 7.5
maxAdjFactorY = maxAdjFactorX
trStatus = None
capx = 1280
capy = 720
adjFactor = 5

cenX = capx/2
cenY = capy/2
#laser_hsv={'hmin': 0, 'smin': 2, 'vmin': 95, 'hmax': 179, 'smax': 185, 'vmax': 255}

cap.set(3, capx)
cap.set(4, capy)
#cap.set(cv2.CAP_PROP_FPS, 50)

theTime = 0
deltaTime = 0

mlen = int(30)
 
fireThread = threading.Thread(target=fire, name="shooter")
centers = deque(maxlen=mlen)
dyncenters = deque(maxlen=mlen)

finder = ColorFinder(False)

fps = FPS()
global rectFrame
rectFrame = None

positionX = 90
positionY = 90

blue = {'hmin': 99, 'smin': 120, 'vmin': 69, 'hmax': 110, 'smax': 192, 'vmax': 212}

yellow = {'hmin': 12, 'smin': 157, 'vmin': 62, 'hmax': 36, 'smax': 252, 'vmax': 255} 

india = {'hmin': 0, 'smin': 89, 'vmin': 57, 'hmax': 17, 'smax': 152, 'vmax': 162} 

green = {'hmin': 31, 'smin': 70, 'vmin': 106, 'hmax': 76, 'smax': 251, 'vmax': 215} # rubix cube

laser = {'hmin': 0, 'smin': 2, 'vmin': 95, 'hmax': 179, 'smax': 185, 'vmax': 255}

hsvVals = 'red'

mousemove = False
dragging = False

currentpt = ()

refPt = []
cropping = None

def adjustPos(cx, cy, adjSize):
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

def click_and_crop(event, x, y, flags, param):
	
	# grab references to the global variables
	global refPt, cropping, rec, finalhsv, mousemove, currentpt, dragging
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN and dragging == False:
		refPt = [(x, y)]
		cropping = True
		dragging = True

	
	elif event == cv2.EVENT_MOUSEMOVE and dragging == True:
		currentpt = (x, y)
		mousemove = True
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP and dragging == True:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		rec = cv2.rectangle(bro1, refPt[0], refPt[1], (0, 255, 0), 2)
		
		dragging = False
		mousemove = False

	elif event == cv2.EVENT_RBUTTONDOWN:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		cropping = True
		finalhsv = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 0, 'smax': 0, 'vmax': 0}
	
		
def doubleline(wndw, contours, centers, trace=True, larRec=True,):
	global theTime
	global trStatus	
	timStat = True
	if contours:
		
		cnzTarea = 0
		largeCnt = None
		for cntZ in contours:
			if (int(cntZ['area']) > cnzTarea):
				cnzTarea = int(cntZ['area']) 
				largeCnt = cntZ
		#print(cnzTarea)
		larCord = largeCnt['bbox']
		if larRec:
			
			wndw = cv2.rectangle(wndw, (larCord[0], larCord[1]), (larCord[0] + larCord[2], larCord[1] + larCord[3]), (200, 0, 128), 2)
			
		#print("area: ", int(contours[0]['area']))
		cx = int(contours[0]['center'][0])
		cy = int(contours[0]['center'][1])

		trStatus = capx/2+math.sqrt(cnzTarea)/2+adjFactor > cx > capx/2-math.sqrt(cnzTarea)/2-adjFactor and capy/2+math.sqrt(cnzTarea)/2+adjFactor > cy > capy/2-math.sqrt(cnzTarea)/2-adjFactor
		print(trStatus)
		if theTime == 0 and trStatus:
			#print("tracking")
			theTime = time.time() 
		
		
		if not trStatus:
			theTime = 0
		#print(largeCnt['area'])
		adjustPos(cx, cy, 0)
		#print(tuple(contours[0]['bbox']))
		modcy = capy - cy
		cv2.line(wndw, (cx, 0), (cx, capy), (0, 255, 0), 2)
		cv2.line(wndw, (0, cy), (capx, cy), (0, 255, 0), 2)

		center = (cx,cy)
		modcen = (cx, modcy)

		loc = "centroid: " + str(modcen) 
		
		#print(loc)

		cv2.putText(wndw,loc, (cx + 10,cy - 10), cv2.FONT_HERSHEY_DUPLEX, .45, (0, 255, 255))
	
		centers.appendleft(center)
		if trace == True:

			for i in range(1, len(centers)):
				# if either of the tracked points are None, ignore
				# them
				if centers[i - 1] is None or centers[i] is None:
					continue
				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = int(np.sqrt(mlen / float(i + 1)) * 2.5)
				cv2.line(wndw, centers[i - 1], centers[i], (0, 0, 255), thickness)

def recCrop(recFrame, contours):

	if contours:
	
		cnzTarea = 0
		largeCnt = None
		for cntZ in contours:
			if (int(cntZ['area']) > cnzTarea):
				cnzTarea = int(cntZ['area']) 
				largeCnt = cntZ
		#print(cnzTarea)
		larCord = largeCnt['bbox']
		
			
		#print(larCord)	
		rectFrame = recFrame[larCord[1]:larCord[1] + larCord[3], larCord[0]:larCord[0] + larCord[2]]
		return rectFrame
	else:
		return recFrame
cv2.namedWindow('dynamic')

finalhsv = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 0, 'smax': 0, 'vmax': 0}

while True:
	k = cv2.waitKey(1)
	win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW))
	success, img= cap.read()
	img = cv2.flip(img, 1)

	rectFrame = img
	#img = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
	imgColor, mask, rawhsv = finder.update(img, hsvVals)
	imgContour, contours = cvzone.findContours(img, mask, minArea=50, c=(0,0,255), xrec=True, drawCon=False)
	center = None
	

	#print(deltaTime)
	

	doubleline(imgContour, contours, centers)
	

	bro, mask1, dynrawhsv = finder.update(img, finalhsv)
	bro1, dyncontours = cvzone.findContours(img, mask1, minArea=50, c=(0,0,255), xrec=False, drawCon=False)	
	cv2.setMouseCallback("dynamic", click_and_crop)
	
	if cropping is False:
		#print(refPt)
		 
		#bro1 = rec
		
		
		
		width = abs(refPt[0][0] - refPt[1][0])

		height =  abs(refPt[0][1] - refPt[1][1])
		
		#print("width: ", width, " height: ", height)

		lxval = [] 
		lyval = []
		allhsv = []
		hVals = []
		sVals = []
		vVals = []

		for tem in range(0, width + 1):
			lxval.append(refPt[0][0] + tem)

		for temy in range(0, height + 1):
			lyval.append(refPt[0][1] + temy)
				
		for xhsv in lxval:
			for yhsv in lyval:
				allhsv.append(dynrawhsv[yhsv, xhsv])


		for hval in allhsv:
			hVals.append(hval[0])

		for sval in allhsv:
			sVals.append(sval[1])

		for vval in allhsv:
			vVals.append(vval[2])

		lower = np.array([min(hVals), min(sVals), min(vVals)])
		upper = np.array([max(hVals), max(sVals), max(vVals)])
		print(lower)
		print(upper)	

		finalhsv = {"hmin": lower[0], "smin": lower[1], "vmin": lower[2],
				   "hmax": upper[0], "smax": upper[1], "vmax": upper[2]}
		print(finalhsv)
		   
		cropping = True

	doubleline(bro1, dyncontours, dyncenters, trace=True)

	rectFrame = recCrop(rectFrame, dyncontours)
	rectFrame = cv2.resize(rectFrame,(426,240))
	deltaTime = time.time() - theTime
	if deltaTime >= 2.5 and trStatus:
		print(deltaTime)
		theTime = 0
		if fireThread.is_alive() == False:
			fireThread = threading.Thread(target=fire, name="shooter")
			fireThread.start()

	if mousemove == True:
		bro1 = cv2.rectangle(bro1, refPt[0], currentpt, (255, 0, 0), 1)

	fps.update(img=bro1)

	#cv2.imshow("preset", imgContour)
	#cv2.imshow("preset - mask", mask)
	#cv2.imshow("preset - raw", imgColor)
	if fireThread.is_alive() == True:

		cv2.putText(bro1,"Firing", (1000 ,70), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0))
	cv2.imshow("dynamic", bro1)
	cv2.imshow("dynamic - mask",  bro)
	cv2.imshow("rectFrame", rectFrame)
	
	

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
		break
	#sock.sendto(str.encode(str(str(positionX)+","+str(positionY))), serverAddressPort) FOR UNITY
cap.release()

cv2.destroyAllWindows()


