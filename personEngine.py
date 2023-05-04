import torch
import cv2
import numpy as np

names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
        'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 
        'teddy bear', 'hair drier', 'toothbrush']

class personTrack:
	def __init__(self, maxPerson=1, modelClasses=0):
		self.maxPerson = maxPerson
		self.modelClasses = modelClasses
		self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
		self.model.classes = modelClasses
	def findPerson(self, img):
		results = self.model(img)
		if len(results.xyxy[0].tolist())>=1:
			obj = results.xyxy[0].tolist()[0]

			x2 = int(obj[0])
			y2 = int(obj[1])
			x1 = int(obj[2])
			y1 = int(obj[3])
			cx = int((x1+x2)/2)
			cy = int((y1+y2)/2)
			x1h = x1 
			y1h = int((y1+y2)/2)
			cxh = int((x2+x1h)/2)
			cyh = int((y2+y1h)/2)

			head = [x1h,y1h,x2,y2,cxh,cyh]

			return x1, y1, x2, y2, cx, cy, head
		else:
			return None,None,None,None,None,None,None

