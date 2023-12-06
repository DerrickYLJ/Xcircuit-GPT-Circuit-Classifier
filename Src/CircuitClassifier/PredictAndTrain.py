

import fastapi
import kaleido
import multipart
import uvicorn
import torch
import torch.nn as nn

import sys
import os


from roboflow import Roboflow
from ultralytics import YOLO

from roboflow import Roboflow

if sys.argv[1] == "predict":    
    model = YOLO('CircuitClassifier/best.pt')
    model.to('cpu')

    predictions = model.predict('../Data/content/Circuit-Segmentation-1/train', save=True, save_txt=True, save_dir='../Data/content/runs/segment/ToDownload/', name='train')
    predictions = model.predict('../Data/content/Circuit-Segmentation-1/valid', save=True, save_txt=True, save_dir='../Data/content/runs/segment/ToDownload/', name='valid')
    predictions = model.predict('../Data/content/Circuit-Segmentation-1/test', save=True, save_txt=True, project ='../Data/content/runs/segment/ToDownload/', name='test')
elif sys.argv[1] == "train":
    rf = Roboflow(api_key="K8P63ZUicTlZO6rZzkQm")
    project = rf.workspace("ethan-muchnik-minqm").project("circuit-segmentation")
    model = YOLO('yolov8n-seg.pt')
    model.to('cpu')
    model.train(data='data.yaml', epochs=100, imgsz=640)
    model.save('best.pt')
elif sys.argv[1] == "predictOne":
    model = YOLO('CircuitClassifier/best.pt')
    model.to('cpu')

    predictions = model.predict(os.path.join('../Data/content/Circuit-Segmentation-1/test/',sys.argv[2]), save=True, save_txt=True, project ='../Data/content/runs/segment/ToDownload/', name='test')




