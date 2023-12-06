import sys
import os

fileToPredict = sys.argv[1]



# Run PredictAndTrain.py
os.system(f"python3 CircuitClassifier/PredictAndTrain.py predictOne {fileToPredict}")

# Run segmentationToOutput.py
os.system("python3 CircuitClassifier/segmentationToOutput.py ../Data/content/runs/segment/ToDownload/test/labels/" + (fileToPredict[:-4] + ".txt"))

os.system("python3 chatGPTInterface/chatgpt_api.py " "tempOutput.txt")







