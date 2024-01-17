import sys
import os
import subprocess

fileToPredict = sys.argv[1]

# Run
result  = subprocess.run("python3 Pipeline-Scene-Classifier/TestScene.py ../Output/SceneDataOutput/ModelWeights/Xception.h5 " + fileToPredict, shell=True, text=True, capture_output=True)
print(result.stdout)
if "Circuit" in result.stdout:
    # Run PredictAndTrain.py
    os.system(f"python3 CircuitClassifier/PredictAndTrain.py predictOne {fileToPredict}")

    # Run segmentationToOutput.py
    os.system("python3 CircuitClassifier/segmentationToOutput.py ../Data/New/content/Circuit-Segmentation-2/test/labels/" + (fileToPredict[:-4] + ".txt"))

    os.system("python3 chatGPTInterface/chatgpt_api.py " "tempOutput.txt")
else:
    print("This extension does not have functionality to process scenes other than circuits")


#print hello world





