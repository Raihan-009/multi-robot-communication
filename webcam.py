import cv2
import random

from http import client
import paho.mqtt.client as paho
import sys

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if ret:
        number = random.random()
        number = int(number*100)
        print(number)
        cv2.imshow("Streaming", frame)
        cli = paho.Client()


        if cli.connect("36.255.69.54", 1883, 60) != 0:
            print("Unable to connect")
            sys.exit(-1)

        cli.publish("test/status", f'Hello from mac hehe {number}', 0)
        cli.disconnect()
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cam.release()