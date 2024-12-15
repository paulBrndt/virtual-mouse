import cv2
import mediapipe as mp
import time
import json
import numpy as np
import pyautogui as auto

path = "IMG_1027"
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Oh nein oh nein!")
    exit()
#cap = cv2.VideoCapture(f"/Users/paulbrendtner/Desktop/Code/dev/latest/mouse/{path}.mp4")

width = int(cap.get(3)) 
height = int(cap.get(4)) 

fourcc = cv2.VideoWriter_fourcc(*"MP4V")
out = cv2.VideoWriter(f"/Users/paulbrendtner/Desktop/Code/dev/latest/mouse/out/{path}.mp4", fourcc, 20.0, (width, height))

def calculateDistance(point1, point2) -> float:
            dx = point1.x - point2.x
            dy = point1.y - point2.y
            dz = point1.z - point2.z
            return np.sqrt(dx**2+dy**2+dz**2)

data = []

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
screen_width, screen_height = auto.size()
distanceOld = False
mouseClick = False
mouseRight = False
analyzeMouse = True
while True:
    success, img = cap.read()
    if not success:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            littleData = {}
            for id, lm in enumerate(handLms.landmark):
                littleData[id] = {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                }
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            data.append(littleData)
        if analyzeMouse:        
            thumbCoor = handLms.landmark[4]
            indexCoor = handLms.landmark[8]
            middleCoor = handLms.landmark[12]
            ringCoor = handLms.landmark[16]
            distanceTM = calculateDistance(thumbCoor, middleCoor)
            distanceTI = calculateDistance(thumbCoor, indexCoor)
            distanceTR = calculateDistance(thumbCoor, ringCoor)
            distanceSmall = True if distanceTM < 0.05 else False
            if distanceSmall:
                auto.moveTo((1 - (thumbCoor.x + middleCoor.x) / 2) * screen_width, ((thumbCoor.y + middleCoor.y) / 2) * screen_height, 0.1)
            if distanceTI < 0.04:
                 if not mouseClick:
                    mouseClick = True
                    auto.click()
            else:
                mouseClick = False
            
            if distanceTR < 0.04:
                if not mouseRight:
                     mouseRight = True
                     auto.rightClick()
            else:
                 mouseRight = False
            
            analyzeMouse = False

        else:
            analyzeMouse = True    

        # landmark_text = [f"ID {id}: ({lm.x:.2f}, {lm.y:.2f}, {lm.z:.2f})" for handLms in results.multi_hand_landmarks for id, lm in enumerate(handLms.landmark)]
        # landmark_text.append(f"Distance {distanceTM}")
        # landmark_text.append("Distance small" if distanceSmall else "")
        # y_offset = 70  # Starting y-coordinate
        # for i, text in enumerate(landmark_text):
        #     cv2.putText(img, text, (10, y_offset + i * 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
        distanceOld = distanceSmall

        

    cTime = time.time()
    fps = 1/(cTime-pTime)
    out.write(img)
    cv2.imshow("Finger detection", img)
    cv2.waitKey(1)
    cTime = time.time()
    pTime = cTime


out.release()


with open("data.json", "w+") as f:
    json.dump(data, f)