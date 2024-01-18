

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

    predictions = model.predict('../Data/Circuit_Data/train', save=True, save_txt=True, save_dir='../Data/', name='train')
    predictions = model.predict('../Data/Circuit_Data/valid', save=True, save_txt=True, save_dir='../Data/', name='valid')
    predictions = model.predict('../Data/Circuit_Data/test', save=True, save_txt=True, project ='../Data/', name='test')
elif sys.argv[1] == "train":
    rf = Roboflow(api_key="K8P63ZUicTlZO6rZzkQm")
    project = rf.workspace("ethan-muchnik-minqm").project("circuit-segmentation")
    model = YOLO('yolov8n-seg.pt')
    model.to('cpu')
    model.train(data='data.yaml', epochs=100, imgsz=640)
    model.save('best.pt')
elif sys.argv[1] == "predictOne": # Currently 
    model = YOLO('CircuitClassifier/best.pt')
    model.to('cpu')

    predictions = model.predict(os.path.join('../Data/',sys.argv[2]), save=True, save_txt=True, project ='../Data/', name='tempLabel')




