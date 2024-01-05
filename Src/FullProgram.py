import sys
import os

fileToPredict = sys.argv[1]


# Run 

# Run PredictAndTrain.py
os.system(f"python3 CircuitClassifier/PredictAndTrain.py predictOne {fileToPredict}")

# Run segmentationToOutput.py
os.system("python3 CircuitClassifier/segmentationToOutput.py ../Data/New/content/Circuit-Segmentation-2/test/labels/" + (fileToPredict[:-4] + ".txt"))

os.system("python3 chatGPTInterface/chatgpt_api.py " "tempOutput.txt")



#print hello world





