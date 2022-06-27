from traceback import print_tb
import cv2
import numpy as np
import math
import time


from http import client
import paho.mqtt.client as paho
import sys
import json

def distance(x1, y1, x2, y2):
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

def find_color1(frame): #green 

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([56, 179, 47])  
    hsv_upperbound = np.array([162, 255, 255]) 
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        #Finding center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # print(cx,cy)
            return (cx, cy), True
        else:
            return (700, 700), False
    else:
        return (700, 700), False 
    
def find_color3(frame): #blue
  
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound =  np.array([110, 71, 0])
    hsv_upperbound = np.array([160, 255, 255])
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        #Finding center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True 
        else:
            return (700, 700), False 
    else:
        return (700, 700), False 
    
def find_color2(frame): #pink

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound =  np.array([165, 101, 75])
    hsv_upperbound = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        #Finding center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True 
        else:
            return (700, 700), False 
    else:
        return (700, 700), False 

data = {}

cap = cv2.VideoCapture(1)

while True:
    _, orig_frame = cap.read()
    #we'll be inplace modifying frames, so save a copy
    copy_frame = orig_frame.copy() 
    (color1_x, color1_y), found_color1 = find_color1(copy_frame)
    (color2_x, color2_y), found_color2 = find_color2(copy_frame)
    (color3_x, color3_y), found_color3 = find_color3(copy_frame)

    #draw circles around these objects
    cv2.circle(copy_frame, (color1_x, color1_y), 20, (255, 0, 0), -1)
    cv2.circle(copy_frame, (color2_x, color2_y), 20, (0, 128, 255), -1)
    cv2.circle(copy_frame, (color3_x, color3_y), 20, (0, 0, 255), -1)


    if found_color2 and (found_color1 or found_color3):
        # print(find_color1)
        # print(find_color2)
        # print(find_color3)
        
        #timestamp counting
        ts = time.time()
        #print(timestamp)
        
        #hypotenuse = distance(color1_x, color1_x, color2_x, color2_y)
        horizontal_distance_one = distance(color1_x, color1_y, color2_x, color2_y)
        #print("Horizontal Distance :", horizontal_distance_one)
        
        horizontal_distance_two = distance(color3_x, color3_y,color2_x, color2_y)
        #print("Horizontal Distance :", horizontal_distance_two)
        #angle = np.arcsin(vertical/hypotenuse)*180.0/math.pi

        data.update({
            "timestamp" : ts,
            "bot1" : horizontal_distance_one,
            "bot2" : horizontal_distance_two })
        
        print(data)
        time.sleep(2)

        cli = paho.Client()

        if cli.connect("36.255.69.54", 1883, 60) != 0:
            print("Unable to connect")
            sys.exit(-1)

        cli.publish("iort", json.dumps(data), 0)
        time.sleep(2)
        cli.disconnect()

        cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 2)
        cv2.line(copy_frame, (color3_x, color3_y), (color2_x, color2_y), (0, 0, 255), 2)
        # cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 2)
        
        cv2.imshow('Distance cal', copy_frame)
        
        if cv2.waitKey(1) & 0xFF  == ord('q'):
            break
    if not found_color2:
        # cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 2)
        # cv2.line(copy_frame, (color3_x, color3_y), (color2_x, color2_y), (0, 0, 255), 2)
        # cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 2)
        
        cv2.imshow('Distance cal', copy_frame)
        
        if cv2.waitKey(1) & 0xFF  == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()