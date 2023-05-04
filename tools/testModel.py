import cv2
import torch
from PIL import Image
from torchvision import transforms
import numpy as np
# Model




model = torch.hub.load('ultralytics/yolov5', 'yolov5s', classes=1)
model = model.to("cuda")
model = model.eval()
model.classes = 0

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
cap = cv2.VideoCapture(0)


ret, frame = cap.read()

frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

print(torch.permute(torch.tensor(frame), (2,0,1)).to('cuda').float().unsqueeze(0).size())


with torch.no_grad():
	rez = model(torch.permute(torch.tensor(frame), (2,0,1)).to('cuda').float().unsqueeze(0))


print(rez[0].tolist()[0])


cv2.waitKey(10000000)


