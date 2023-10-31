!pip install ultralytics
!pip install roboflow
!pip install fastapi
!pip install kaleido
!pip install multipart
!pip install uvicorn

import fastapi
import kaleido
import multipart
import uvicorn
import torch
import torch.nn as nn




from roboflow import Roboflow
from ultralytics import YOLO

# model = YOLO("yolov8n.pt")  # load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')


rf = Roboflow(api_key="K8P63ZUicTlZO6rZzkQm")
project = rf.workspace("ethan-muchnik-minqm").project("wires-3ev6e")
dataset = project.version(1).download("yolov8")

model.train(data='/content/Wires-1/data.yaml', epochs=100, imgsz=640)