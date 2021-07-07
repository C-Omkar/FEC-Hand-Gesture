####################### IMPORT MODULES #######################
## If you wnat to add any more python modules Add here      ##
##############################################################
from typing import OrderedDict
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
# If want to add some feature list that you might want to use while cheking add here
# shapes = {}

##############################################################


def scan_image(img_file_path):

    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img_file_path)
    """


    # global shapes
    shapes = {}

    ##############	ADD YOUR CODE HERE	##############
    img_file_path = str(img_file_path)
    img = cv2.imread(img_file_path, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Ranges of Red, Green, Blue
    red_lower = np.array([0, 70, 50], np.uint8)
    red_upper = np.array([10, 255, 255], np.uint8)
    # red_lower1 = np.array([170, 70, 50], np.uint8)
    # red_lower2 = np.array([180, 255, 255], np.uint8)
    red_mask1 = cv2.inRange(hsv, red_lower, red_upper)
    # red_mask2 = cv2.inRange(hsv, red_lower1, red_lower2)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)


    lower_range = np.array([0, 2, 0], np.uint8)
    upper_range = np.array([179, 255, 255], np.uint8)
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Red
    contours1, heirarchy = cv2.findContours(red_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # contours2, heirarchy = cv2.findContours(red_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours1):
        lst = []
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(img, "Red Color", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0,0,255))
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            
            # Calculating Moments for Each Contour
            M = cv2.moments(contour)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(img, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)

            if len(approx) == 3:
                Shape = "Triangle"
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h) # Slope
                a = ((approx[0][0][0] - approx[1][0][0])**2 + (approx[0][0][1] - approx[1][0][1])**2)**(1/2)
                a_slope = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0] + 0.01)
                b = ((approx[1][0][0] - approx[2][0][0])**2 + (approx[1][0][1] - approx[2][0][1])**2)**(1/2)
                b_slope = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0] + 0.01)
                c = ((approx[2][0][0] - approx[3][0][0])**2 + (approx[2][0][1] - approx[3][0][1])**2)**(1/2)
                c_slope = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0] + 0.01)
                d = ((approx[3][0][0] - approx[0][0][0])**2 + (approx[3][0][1] - approx[0][0][1])**2)**(1/2)
                d_slope = (approx[0][0][1] - approx[3][0][1]) / (approx[0][0][0] - approx[3][0][0] + 0.01)
                if ar >= 0.95 and ar <= 1.05:
                    Shape = "Square"
                    # print(approx, a, b, c, d)
                elif abs(a-b) < 5 and abs(b-c) < 5 and abs(c-d) < 5 and abs(d-a) < 5:
                    Shape = "Rhombus"
                elif (abs(a_slope - c_slope) < 0.04 and abs(b_slope - d_slope) > 0.04) or (abs(a_slope - c_slope) > 0.04 and abs(b_slope - d_slope) < 0.04):
                    Shape = "Trapezium"
                else:
                    Shape = "Quadrilateral"
            elif len(approx) == 5:
                Shape = "Pentagon"
            elif len(approx) == 6:
                Shape = "Hexagon"
            else:
                Shape = "Circle"
            color = "Red"
            lst.append(color)
            lst.append(area)
            lst.append(cX)
            lst.append(cY)

            shapes[Shape] = lst



    # Green
    contours, heirarchy = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours):
        lst = []
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(img, "Green Color", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0,0,255))
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            # Calculating Moments for Each Contour
            M = cv2.moments(contour)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(img, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
            if len(approx) == 3:
                Shape = "Triangle"
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                a = ((approx[0][0][0] - approx[1][0][0])**2 + (approx[0][0][1] - approx[1][0][1])**2)**(1/2)
                a_slope = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0] + 0.01)
                b = ((approx[1][0][0] - approx[2][0][0])**2 + (approx[1][0][1] - approx[2][0][1])**2)**(1/2)
                b_slope = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0] + 0.01)
                c = ((approx[2][0][0] - approx[3][0][0])**2 + (approx[2][0][1] - approx[3][0][1])**2)**(1/2)
                c_slope = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0] + 0.01)
                d = ((approx[3][0][0] - approx[0][0][0])**2 + (approx[3][0][1] - approx[0][0][1])**2)**(1/2)
                d_slope = (approx[0][0][1] - approx[3][0][1]) / (approx[0][0][0] - approx[3][0][0] + 0.01)
                if ar >= 0.95 and ar <= 1.05:
                    Shape = "Square"
                    # print(approx, a, b, c, d)
                elif abs(a-b) < 5 and abs(b-c) < 5 and abs(c-d) < 5 and abs(d-a) < 5:
                    Shape = "Rhombus"
                elif (abs(a_slope - c_slope) < 0.04 and abs(b_slope - d_slope) > 0.04) or (abs(a_slope - c_slope) > 0.04 and abs(b_slope - d_slope) < 0.04):
                    Shape = "Trapezium"
                else:
                    Shape = "Quadrilateral"
            elif len(approx) == 5:
                Shape = "Pentagon"
            elif len(approx) == 6:
                Shape = "Hexagon"
            else:
                Shape = "Circle"
            color = "Green"
            lst.append(color)
            lst.append(area)
            lst.append(cX)
            lst.append(cY)

            shapes[Shape] = lst

            # print(approx)

    # Blue
    contours, heirarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        lst = []
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, "Blue Color", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            # Calculating Moments for Each Contour
            M = cv2.moments(contour)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(img, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
            if len(approx) == 3:
                Shape = "Triangle"
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                a = ((approx[0][0][0] - approx[1][0][0])**2 + (approx[0][0][1] - approx[1][0][1])**2)**(1/2)
                a_slope = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0] + 0.01)
                b = ((approx[1][0][0] - approx[2][0][0])**2 + (approx[1][0][1] - approx[2][0][1])**2)**(1/2)
                b_slope = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0] + 0.01)
                c = ((approx[2][0][0] - approx[3][0][0])**2 + (approx[2][0][1] - approx[3][0][1])**2)**(1/2)
                c_slope = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0] + 0.01)
                d = ((approx[3][0][0] - approx[0][0][0])**2 + (approx[3][0][1] - approx[0][0][1])**2)**(1/2)
                d_slope = (approx[0][0][1] - approx[3][0][1]) / (approx[0][0][0] - approx[3][0][0] + 0.01)
                # print(a_slope, b_slope, c_slope, d_slope)
                if ar >= 0.95 and ar <= 1.05:
                    Shape = "Square"
                    # print(approx, a, b, c, d)
                elif abs(a-b) < 10 and abs(b-c) < 10 and abs(c-d) < 10 and abs(d-a) < 10:
                    Shape = "Rhombus"
                elif (abs(a_slope - c_slope) < 0.04 and abs(b_slope - d_slope) > 0.04) or (abs(a_slope - c_slope) > 0.04 and abs(b_slope - d_slope) < 0.04):
                    Shape = "Trapezium"
                else:
                    Shape = "Quadrilateral"
            elif len(approx) == 5:
                Shape = "Pentagon"
            elif len(approx) == 6:
                Shape = "Hexagon"
            else:
                Shape = "Circle"
            color = "Blue"
            lst.append(color)
            lst.append(area)
            lst.append(cX)
            lst.append(cY)

            shapes[Shape] = lst
         


    # SHAPE DETECTION
    
    # https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)

    # First Contour is the shape of image. We will ignore it.

    
    # count = 0
    # for contour in contours:
    #     if count == 0:
    #         count = 1
    #         continue

    #     approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # print(approx)

        # cv2.drawContours(img, [contour], 0, (0, 0, 0), 5)

        # if len(approx_count) == 3:
        #     Triangle
        # elif len(approx_count) == 4:
        #     Rectangle
        # elif len(approx_count) == 5:
        #     Pentagon
        # elif len(approx_count) == 6:
        #     Hexagon
        # else:
        #     Circle
            
        
    # cv2.imshow('Image', img)
    # cv2.imshow('Mask', mask)
    cv2.waitKey(0)
    # img.release()
    cv2.destroyAllWindows

	##################################################
    
    return shapes


# Here No need to make any changes if you are running the code in the folder's directory
# Only complete the function scan_images carefully with all the specifications met
# In main Most part of code is just to scan the file from directory correctly
# print(scan_image('Desktop/Samples/Sample4.png'))
if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 4
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')