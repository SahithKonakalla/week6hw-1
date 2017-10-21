
# coding: utf-8

# In[ ]:

import cv2
import numpy as np
import math

def angle(p1, p2, p0):
   dx1 = p1[0][0]-p0[0][0]
   dy1 = p1[0][1]-p0[0][1]
   dx2 = p2[0][0]-p0[0][0]
   dy2 = p2[0][1]-p0[0][1]
   return math.atan(dy1/dx1)-math.atan(dy2/dx2)

def right(app, x):
    maxCosine = 0
    for k in range(2, x+1):
        if (len(app) == x):
            pt1 = app[k%4]
            pt2 = app[k-2]
            pt0 = app[k-1]
            cos = (angle(pt1, pt2, pt0))
            cosine = math.fabs(math.cos(cos))
            maxCosine = max(maxCosine, cosine)
            if(maxCosine<10):
                print (maxCosine)
                return True
            else:
                return False
        else:
            return False
        

img = cv2.imread("rectangle-five-feet.jpg") #Reads image and places it into img

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Converts to HSV

#cv2.imshow("HSV", img_hsv)

THRESHOLD_MIN = np.array([20, 0, 235],np.uint8) # Sets minimum hue
THRESHOLD_MAX = np.array([100, 255, 255],np.uint8) # Sets maximum hue

thresh = cv2.inRange(img_hsv, THRESHOLD_MIN, THRESHOLD_MAX)

cv2.imshow("Thresholded", thresh)

cannied = cv2.Canny(thresh, 0, 20, 3)

cv2.imshow("Canny", cannied)

(edges, _) = cv2.findContours(cannied, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

epsilon = 0.1*cv2.arcLength(edges[0],True)
highArea = cv2.contourArea(cv2.approxPolyDP(edges[0], epsilon, True))
print(len(edges))
for i in edges:
    epsilon = 0.1*cv2.arcLength(i,True)
    approx = cv2.approxPolyDP(i, epsilon, True)
    area = cv2.contourArea(approx)
    if (len(approx)==4 and area > 300):
        highArea = area
        final = approx
        found = True
print (final)
final2 = [final]
if found:
    cv2.drawContours(img, final2, 0, (0,255,255), 10)
    #print (highArea)
    #print ("drew")
    
    avgX = 0
    avgY = 0
    temp = final[0]
    minX = temp[0][0]
    maxX = temp[0][0]
    minY = temp[0][1]
    maxY = temp[0][1]
    for p in final:  
        if p[0][0] < minX:
            minX = p[0][0]
        if p[0][0] > maxX:
            maxX = p[0][0]
        if p[0][1] < minY:
            minY = p[0][1]
        if p[0][1] > maxY:
            maxY = p[0][1]
        
    widthX = maxX-minX
    widthY = maxY-minY
    avgX = (maxX+minX)/2
    avgY = (maxY+minY)/2
    

imgW, imgH = img_hsv.shape[:2]
print (imgW)
#print (imgH)
print (avgX)
print (widthX)
distance = (480*0.1)/widthX
#azimuth = (math.atan((double)(avgX) -(double)(widthX/2))/ 480) * (math.pi/180)
#altitude = (math.atan((double)(avgY) -(double)(widthY/2))/ 480) * (math.pi/180)
azimuth = (math.atan((avgX -240)/ 480)) * (180/3.14)
altitude = (math.atan((avgY - 240)/ 480)) * (180/3.14)

print distance
print azimuth
print altitude

print ("done")
cv2.imshow("Done", img)

cv2.waitKey(0)






# In[ ]:




# In[ ]:




# In[ ]:



