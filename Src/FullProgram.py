import sys
import os
import subprocess

fileToPredict = sys.argv[1]

# All file names should be from Scene Data as root
result  = subprocess.run("python3 Pipeline-Scene-Classifier/TestScene.py ../Output/SceneDataOutput/ModelWeights/Xception.h5 " + fileToPredict, shell=True, text=True, capture_output=True)
print(result.stdout)
if "Circuit" in result.stdout:
    # Run PredictAndTrain.py
    os.system("python3 CircuitClassifier/PredictAndTrain.py predictOne Scene_Data/" + fileToPredict)

    # Run segmentationToOutput.py
    os.system("python3 CircuitClassifier/segmentationToOutput.py ../Data/tempLabel/labels/" + (os.path.basename(fileToPredict)[:-4] + ".txt"))

    os.system("python3 chatGPTInterface/chatgpt_api.py " "tempOutput.txt")

    # remove templabel
    os.system("rm -rf ../Data/tempLabel")
else:
    print("This extension does not have functionality to process scenes other than circuits")


#print hello world





