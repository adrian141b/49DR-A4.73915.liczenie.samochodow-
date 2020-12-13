import cv2
import numpy as np
from time import sleep

lengt_min = 10
height_min = 10
lengt_max = 100
height_max = 100
survey = 4
line = 300
cars =0
speed = 60
detec = []



def count_line(x, y, w, h):
    cx = x + w
    cy = y + h
    return cx, cy


cap = cv2.VideoCapture('test')
subtrac = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame1 = cap.read()
    rate = float(1 / speed)
    sleep(rate)
    bgr2gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blue = cv2.GaussianBlur(bgr2gray, (3, 3), 0)
    img_sub = subtrac.apply(blue)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    outline, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (0, line), (250, line), (255, 255, 255), 3)
    for (i, c) in enumerate(outline):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_outline = (w >= lengt_min) and (h >= height_min) and (w <= lengt_max) and ( w <= height_max)
        if not validar_outline:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        point = count_line(x, y, w, h)
        detec.append(point)
        cv2.circle(frame1, point, 4, (0, 0, 255), -1)

        for (x, y) in detec:
            if y < (line + survey) and y > (line - survey):
                cars += 1
                cv2.line(frame1, (0, line), (250, line), (0, 0, 255), 3)
                detec.remove((x, y))
                print("samochód : " + str(cars))

    cv2.imshow("obraz", frame1)
    cv2.imshow("obraz z openCV", dilat)

    if cv2.waitKey(1) == 0:
        break

cv2.destroyAllWindows()
cap.release()
