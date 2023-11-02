import sys
import os
import matplotlib.pyplot as plt
from typing import Callable

# Label to Object
labelToObject = {
    0: "Battery",
    1: "Capacitor",
    2: "Light Bulb",
    3: "Resistor",
    4: "Wire"
}

# Result Class

class Result:
    falsePositive = 0
    falseNegative = 0
    truePositive = 0
    def __init__(self, falsePositive, falseNegative, truePositive):
        self.falsePositive = falsePositive
        self.falseNegative = falseNegative
        self.truePositive = truePositive

    def getPrecision(self):
        return self.truePositive/(self.truePositive + self.falsePositive)
    
    def getRecall(self):
        return self.truePositive/(self.truePositive + self.falseNegative)

# read from label files
class ImageLabel:
    labels = []
    fileName = ""
    def __init__(self, labels):

        # label is a list of strings. get each strin up until first space
        self.labels = list(map(lambda x: x.split()[0], labels[1]))
        self.fileName = labels[0]
        

        

def readLabels(folder):
    # open each file in label folder and read lines into a buffer. Have list of contents of files
    labels = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file)) as f:
                lines = f.readlines()

                labels.append((file,lines))

    return labels


def compareLabels(labelOriginal, labelResult):
    print(labelOriginal.fileName, labelResult.fileName)
    print(len(labelOriginal.labels), len(labelResult.labels))
    # assert(len(labelOriginal.labels) == len(labelResult.labels))
    # compare two lists of labels. return a list of labels that are in both lists

    listOriginalFreq = [0]*len(labelToObject)
    listResultFreq = [0]*len(labelToObject)

    truePositive = 0
    falsePositive = 0
    falseNegative = 0

    for i in range(len(labelOriginal.labels)):
        listOriginalFreq[int(labelOriginal.labels[i])] +=1
    
    for i in range(len(labelResult.labels)):
        listResultFreq[int(labelResult.labels[i])] +=1

    print("listOriginalFreqResultFreq")
    print(listOriginalFreq)
    print(listResultFreq)
    for i in range(len(listOriginalFreq)):
        diff = listOriginalFreq[i] - listResultFreq[i]
        if diff < 0:
            falsePositive += abs(diff)
            truePositive += listOriginalFreq[i]
        elif diff > 0:
            falseNegative += diff
            truePositive += listResultFreq[i]
        else:
            truePositive += listOriginalFreq[i]

    print("falsePositive: ", falsePositive)
    print("falseNegative: ", falseNegative)
    print("truePositive: ", truePositive)
    print("soceity: ")
            
    return Result(falsePositive, falseNegative, truePositive)

# matplot lib graph
def createMatplotLibBarGraph(listTrain, listTest, listValidation, argumentVal):

    if argumentVal == "precision":
        categories = ["Train", "Test", "Validation"]
        print("list tarin length: ", len(listTrain))
        print("list test length: ", len(listTest))
        print("list validation length: ", len(listValidation))
        
        # print(type(listTrain[0]))
        # print(len(listTrain))
        getPrecision: Callable[[Result], float] = lambda x: x.getPrecision()
        # print("hi")
        # for i in range(len(listTrain)):
        #     print(listTrain[i].getPrecision())
        # print("sup")

        values = [sum(list(map(getPrecision, listTrain)))/len(listTrain), sum(list(map(lambda x : x.getPrecision(),listTest)))/len(listTest), sum(list(map(lambda x : x.getPrecision(), listValidation)))/len(listValidation)]

        plt.bar(categories, values)

        #add value labels
        for i in range(len(values)):
            plt.text(i, values[i], str(round(values[i], 2)))

        # Adding labels and a title
        plt.xlabel('Train/Test/Validation')
        plt.ylabel('Percentage Correct')
        plt.title('Percentage of Box Label Correct')

        plt.show()
    elif argumentVal == "recall":
        categories = ["Train", "Test", "Validation"]
        print("list tarin length: ", len(listTrain))
        print("list test length: ", len(listTest))
        print("list validation length: ", len(listValidation))
        
        # print(type(listTrain[0]))
        # print(len(listTrain))
        getRecall: Callable[[Result], float] = lambda x: x.getRecall()
        # print("hi")
        # for i in range(len(listTrain)):
        #     print(listTrain[i].getPrecision())
        # print("sup")

        values = [sum(list(map(getRecall, listTrain)))/len(listTrain), sum(list(map(lambda x : x.getRecall(),listTest)))/len(listTest), sum(list(map(lambda x : x.getRecall(), listValidation)))/len(listValidation)]

        plt.bar(categories, values)

        #add value labels
        for i in range(len(values)):
            plt.text(i, values[i], str(round(values[i], 2)))

        # Adding labels and a title
        plt.xlabel('Train/Test/Validation')
        plt.ylabel('Percentage Correct')
        plt.title('Percentage of Box Label Correct')

        plt.show()
    elif argumentVal == "chatGPT":
        categories = ["Helpful", "Unhelpful"]
        helpful = 10
        unhelpful = 4
        
        values = [helpful, unhelpful]

        # Create pi chart
        plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    
# See value of argument supplied to python file
argumentVal = sys.argv[1]

trainImgs = readLabels("../../Data/Labelled-Images/content/Wires-1/train/labels")
testImgs = readLabels("../../Data/Labelled-Images/content/Wires-1/test/labels")
validationImgs = readLabels("../../Data/Labelled-Images/content/Wires-1/valid/labels")

trainResImgs = readLabels("../../Data/Generated-Results/TrainSet/labels")
testResImgs = readLabels("../../Data/Generated-Results/TestSet/labels")
validationResImgs = readLabels("../../Data/Generated-Results/ValidSet/labels")

#combine trainImgs, testImgs, and validationImgs into one list of labels
originalLabels = (list(map( lambda x: ImageLabel(x),trainImgs)), list(map( lambda x: ImageLabel(x),testImgs)), list(map( lambda x: ImageLabel(x),validationImgs)))
generatedLabels = (list(map( lambda x: ImageLabel(x),trainResImgs)), list(map( lambda x: ImageLabel(x),testResImgs)), list(map( lambda x: ImageLabel(x),validationResImgs)))

compareListTrain = []
compareListTest = []
compareListValidation = []

for i in range(len(originalLabels)):
    for j in range(len(originalLabels[i])):
        res = (compareLabels(originalLabels[i][j], generatedLabels[i][j]))
        if i == 0:
            compareListTrain.append(res)
        elif i == 1:
            compareListTest.append(res)
        else:
            compareListValidation.append(res)

createMatplotLibBarGraph(compareListTrain, compareListTest, compareListValidation, argumentVal)

