# GPT Circuit Classifier

This repo consists of code to allow chatgpt to effectively classify images of circuits. This algoirthm consists of several steps. First a scene is classified. If it is a circuit, then YOLO uses CNNs to draw segmentations around various items. Then an algorithm uses said segmentations to essentially convert the image to a sentence describing the circuit which will be fed into chatgpt. The response from chatgpt is the final output.

- Data: The original image data
- Output: The ouput images from YOLO segmentation algorithm
- Circuit Classifier: Has Code involved with Training and Using Segmentation algorithm. 
    - PredictAndTrain.py: Predicts or Trains Yolo algorithm
    - segmentationToOutput.py: converts segmentation output to chatgpt text input
    - boundingBoxToOutput.py: No longer used but converted bounding boxes around objects to chatgpt input
    - best.pt: Best performing yolo model weights
- Graph Generation: Generates Matplotlib Graphs For Paper
- chatGPTInterface: Utilizes chatGPT by feeding input text and printing output text
- FullProgram.py: Runs algorithm from YOLO to chatgpt Output