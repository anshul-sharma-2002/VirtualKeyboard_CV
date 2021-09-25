import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

finalText = "Output : "

keyboard = Controller()

def drawAll(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 130, 20), cv2.FILLED)
        cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button((100 * j + 100, 100 * i + 50), key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmlist:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:
                cv2.rectangle(img, (x-5, y-5), (x + w +5, y + h +5), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 40:
                    keyboard.press(button.text)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.25)

    cv2.rectangle(img, (100, 350), (1100, 420), (255, 130, 20), cv2.FILLED)
    cv2.putText(img, finalText, (110, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)