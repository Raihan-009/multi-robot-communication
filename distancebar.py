import cv2
import numpy as np
import math
from datetime import datetime

def distance(x1, y1, x2, y2):
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

def find_color1(frame): #pink 
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([141, 51, 204]) #replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([179, 255, 255])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        #Find center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True
        else:
            return (700, 700), False #faraway point
    else:
        return (700, 700), False #faraway point
    
def find_color3(frame): #Yellow
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound =  np.array([0, 175, 204])#replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([74, 255, 255])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        #Find center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True #True
        else:
            return (700, 700), True #faraway point
    else:
        return (700, 700), True #faraway point
    
def find_color2(frame): #White
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound =  np.array([0, 0, 180])#replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([111, 52, 255])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        #Find center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True #True
        else:
            return (700, 700), True #faraway point
    else:
        return (700, 700), True #faraway point

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

    if found_color1 and found_color2 and found_color3:
        
        time = datetime.now()
        #print(time)
        #trig stuff to get the line
        # hypotenuse = distance(color1_x, color1_x, color2_x, color2_y)
        horizontal_distance_one = distance(color1_x, color1_y, color2_x, color1_y)
        #print("Horizontal Distance :", horizontal_distance_one)
        
        horizontal_distance_two = distance(color3_x, color3_y, color2_x, color1_y)
        #print("Horizontal Distance :", horizontal_distance_two)
        # angle = np.arcsin(vertical/hypotenuse)*180.0/math.pi

        data.update({
            "time " : time,
            "bot1 " : horizontal_distance_one,
            "bot2 " : horizontal_distance_two })
        
        print(data)
        #draw all 3 lines
        cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 2)
        cv2.line(copy_frame, (color3_x, color3_y), (color2_x, color1_y), (0, 0, 255), 2)
        # cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 2)
        
        cv2.imshow('Distance cal', copy_frame)
        
        if cv2.waitKey(1) & 0xFF  == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()