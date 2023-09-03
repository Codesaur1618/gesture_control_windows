import cv2
import time
import handtracking as htm
import numpy as np
import math
import screen_brightness_control as sbc

################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = htm.handDetector(detect_con=0.7)
maxB = 100
minB = 0

while True:
    success, img = cap.read()
    img = detector.find_Hands(img)
    Landmark_list = detector.locateHands(img, draw=False)
    label = detector.get_label(img)
    if len(Landmark_list) != 0:
        # print(Landmark_list[4], Landmark_list[8])
        x1, y1 = Landmark_list[4][1], Landmark_list[4][2]
        x2, y2 = Landmark_list[8][1], Landmark_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        # Hand Range --  250 - 20
        # Brightness Range = 0- 100

        brightness = np.interp(length, [20, 250], [minB, maxB])
        sbc.set_brightness(brightness)
        cv2.line(img, (50, 430), (50, 430 - int(length)), (0, 255, 0), 4)
        cv2.putText(img, f'{int(brightness)} %', (cx + 5, cy), cv2.QT_FONT_NORMAL,
                    0.5, (0, 255, 0), 2)

        x3, y3 = Landmark_list[0][1], Landmark_list[0][2]
        cv2.putText(img, str(label), (x3, y3+20), cv2.QT_FONT_NORMAL,
                    0.5, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,  50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)