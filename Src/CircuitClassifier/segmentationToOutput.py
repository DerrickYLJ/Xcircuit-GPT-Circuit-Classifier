# Read From File

import sys
import os
import shapely.geometry as Polygon

# Label to Object
labelToObject = {
    0: "Battery",
    1: "Light Bulb",
    2: "Resistor",
    3: "Wire",
    4: "Battery On Fire"
}


class BoundingBox:
    XYList = []
    id = 0
    label = 0

    def __init__(self,label,cordsXYTuple, id ):
        self.XYList = cordsXYTuple
        self.id = id
        self.label = label

# Read from file
def readFromFile(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

# Seperate Each Line Into List Of Words
def seperateLines(lines):
    seperateLines = []
    for line in lines:
        seperateLines.append(line.split())
    BoundingBoxList = []
    id = 0
    for line in seperateLines:
        #convert string to list of tuples
        cords = line[1:]
        cordsXYTuple = []
        for i in range(0, len(cords), 2):
            cordsXYTuple.append((float(cords[i]), float(cords[i+1])))
        BoundingBoxList.append(BoundingBox(int(line[0]),cordsXYTuple, id))
        id += 1
        
    return BoundingBoxList
def calculate_overlap(currBoxCordsList, otherBoxCordsList):
    currBox = Polygon.Polygon(currBoxCordsList)
    otherBox = Polygon.Polygon(otherBoxCordsList)
    intersection = currBox.intersection(otherBox)
    distance = currBox.distance(otherBox)
    print("intersection area is: " + str(intersection.area))
    return intersection.area, distance


def getGroupsOfConnectedBoxes(BoxList):
    groups = []
    disconnected = []
    fullLoop = []
    # Start at each box and find connected boxes in one direction
    for i in range(len(BoxList)):
        # Create a new group
        groups.append([BoxList[i]])

        # disconnected
        disconnected.append([])

         # ID already used
        used = [BoxList[i].id]
        # Find the next box in the same direction until there are no more unused boxes connected to the last box
        currBox = BoxList[i]
        if len(used) == len(BoxList):
            fullLoop.append(True)
            break
        while True:
            setOfOverlappingUnusedBoxe = set()
            setOfOverlappingBoxes = set()
            for j in range(len(BoxList)):
                if j == currBox.id:
                    continue
                overLapAmm, distance = calculate_overlap(currBox.XYList,BoxList[j].XYList)
                if overLapAmm > 0.001 or distance < 0.05:
                    setOfOverlappingBoxes.add(BoxList[j].id)
                    if BoxList[j].id not in used:
                        setOfOverlappingUnusedBoxe.add((BoxList[j].id, overLapAmm))

            # print("here once")
            if len(setOfOverlappingUnusedBoxe) != 0:
                # Get ID with largest overlap
                maxOverLapID = max(setOfOverlappingUnusedBoxe, key=lambda x:x[1])[0]
                # Add this box to the group            
                groups[-1].append(BoxList[maxOverLapID])
                # Mark this box as used
                used.append(maxOverLapID)
                # Set this box as the current box
                currBox = BoxList[maxOverLapID]
            else:
                # print("society")
                #convert setOfOverlappingUnusedBoxe to set of just id
                if BoxList[i].id in setOfOverlappingBoxes:
                    fullLoop.append(True)
                else:
                    fullLoop.append(False)

                setOfOverlappingUnused = set()
                for j in setOfOverlappingUnusedBoxe:
                    setOfOverlappingUnused.add(BoxList[j].id)
                
                # Add the disconnected boxes to the disconnected list
                for j in range(len(BoxList)):
                    if BoxList[j].id not in used and BoxList[j].id not in setOfOverlappingUnused:
                        disconnected[-1].append(BoxList[j])
                break
            if len(used) == len(BoxList):
                print("this group is: " + str(list(map( lambda x: x.id ,groups[-1]))))
                print("id of i is: " + str(BoxList[i].id))
                print("The overlapping boxes are: " + str(setOfOverlappingBoxes))
                setOfOverlappingBoxes = set()
                for j in range(len(BoxList)):
                    if j == currBox.id:
                        continue
                    overLapAmm, distance = calculate_overlap(currBox.XYList,BoxList[j].XYList)
                    print("distance is: " + str(distance))
                    print("overlap amm is: " + str(overLapAmm))
                    if overLapAmm > 0.000 or distance < 0.03:
                        setOfOverlappingBoxes.add(BoxList[j].id)
                if BoxList[i].id in setOfOverlappingBoxes:
                    fullLoop.append(True)
                else:
                    fullLoop.append(False)
                break


            # print(createDictForBoxesFromID[currBox.id].x)
        

    # print list  containing lengths of each of the lists
    print([len(group) for group in groups])
    print([len(dis) for dis in disconnected])
    print(fullLoop)

    
    return (groups, disconnected, fullLoop)



lines = readFromFile(sys.argv[1])

BoundingBoxList = seperateLines(lines)

createDictForBoxesFromID = {}
for box in BoundingBoxList:
    createDictForBoxesFromID[box.id] = box


groups, disconnected, fullLoop = getGroupsOfConnectedBoxes(BoundingBoxList)

# return list with the longest length for each group and the index of it
def getLongestGroupThatsTrue(groups, fullLoop):
    longest = 0
    longestIndex = 0
    for i in range(len(groups)):
        if len(groups[i]) > longest and fullLoop[i]:
            longest = len(groups[i])
            longestIndex = i
    return (longest, longestIndex)



# create prompt for said list
def createPromptForGroup(group, disconnected, fullLoop):
    prompt = ""
    prompt += "Will components create a complete circuit that works and have no major risks?\n\n"
    if len(group) != 0:
        if len(group) > 1:
            prompt += "There is a "
            for i in range(len(group)):
                if i == len(group) - 1:
                    if fullLoop:
                        prompt = prompt[:-16] + " connected to a " + labelToObject[group[i].label] + " connected to the original "  + labelToObject[group[0].label]
                    else:
                        prompt = prompt[:-16] + " connected to a " + labelToObject[group[i].label] + " not connected to the original " + labelToObject[group[0].label]
                else:
                    prompt += labelToObject[group[i].label] + " connected to a "

            prompt += ".\n\n"
            # print("The prompt is: " + prompt)
            
            # if len(disconnected) >= 1:
            #     prompt += "There are also additional disconnected components of a " + labelToObject[disconnected[0].label] 
            #     for i in range(1, len(disconnected)):
            #         if i == len(disconnected) - 1:
            #             prompt += " and a " + labelToObject[disconnected[i].label]
            #         else:
            #             prompt += ", a " + labelToObject[disconnected[i].label]
                
            #     prompt += ".\n\n"
        else:
            prompt += "There is a " + labelToObject[group[0].label] + ".\n\n"
            # if len(disconnected) >= 1:
            #     prompt += "There are also additional disconnected components of a " + labelToObject[disconnected[0].label] 
            #     for i in range(1, len(disconnected)):
            #         if i == len(disconnected) - 1:
            #             prompt += " and a " + labelToObject[disconnected[i].label]
            #         else:
            #             prompt += ", a " + labelToObject[disconnected[i].label]
                
            #     prompt += ".\n\n"
        
    else:
        prompt += "There are no components connected to each other."
    

    return prompt


longest, longestIndex = getLongestGroupThatsTrue(groups, fullLoop)

# print("The longest group is: " + str(longest))
# print("The index of the longest group is: " + str(longestIndex))
# print("length of disconnected is: " + str(len(disconnected)))
# print("length of fullLoop is: " + str(len(fullLoop)))
prompt = createPromptForGroup(groups[longestIndex], disconnected[longestIndex], fullLoop[longestIndex])
# print("THIS IS ORGIINAL PROMPT:" + prompt)

# output to file
outputFile = open("tempOutput.txt", "w")
outputFile.write(prompt)
