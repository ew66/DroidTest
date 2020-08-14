#!/usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
import random

matching_methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

def get_image(image_name):
    img = cv2.imread(image_name)
    return img

def get_image_from_byte(image_byte):
    nparr = np.fromstring(image_byte, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_matching_result(template, img, method):
#    img = cv2.imread(image_name, 1)
#    img2 = pattern_img.copy()
#    template = cv2.imread(pattern_name, 1)
    h, w, ch = template.shape[::]
    if method not in matching_methods:
        use_method = eval('cv2.TM_CCOEFF_NORMED')
    else:
        use_method = eval(method)

    # Apply template Matching
    t1 = cv2.getTickCount()
    res = cv2.matchTemplate(img,template,use_method)
    t2 = cv2.getTickCount()
    time = (t2 - t1) / cv2.getTickFrequency()
    #print "Use " + method + " cost " + str(time) + "s"

    
    #return result image
    #print "done."
    return res

def is_pattern_in_image2(pattern, image, method, threshold, save_result):
    result_img = get_matching_result(pattern, image, method)
    result_loc = np.where(result_img >= threshold)
    #print result_loc
    result_pt = list(zip(*result_loc[::-1]))
    #print result_pt
    if bool(result_pt):
        if save_result:
            res_img = image.copy()
            h, w, ch = pattern.shape[::]
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_img)
            #print min_val, max_val, min_loc, max_loc
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if eval(method) in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(res_img,top_left, bottom_right, [0,0,255], 20)
            #cv2.imwrite("./result_img.png", res_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        
            return True 

    return False

def is_pattern_in_image(pattern_name, image_name, method, threshold, save_result):
    image = get_image(image_name)
    pattern = get_image(pattern_name)
    result_img = get_matching_result(pattern, image, method)
    result_loc = np.where(result_img >= threshold)
    #print result_loc
    result_pt = list(zip(*result_loc[::-1]))
    #print result_pt
    if bool(result_pt):
        if save_result:
            res_img = image.copy()
            h, w, ch = pattern.shape[::]
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_img)
            #print min_val, max_val, min_loc, max_loc
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if eval(method) in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(res_img,top_left, bottom_right, [0,0,255], 20)
            cv2.imwrite("./result_img.png", res_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        
            return True 

    return False
    #return yes or no

if __name__ == '__main__':
    threshold = 0.95
    save_rst = True
    print(("is template_error.png in error_result.png? ", is_pattern_in_image('template_error.png', 'result_img.png', 'cv2.TM_CCOEFF_NORMED', threshold, save_rst)))
#    print "is template_error.png in error_result.png? ", is_pattern_in_image('template_error.png', 'error_result.png', 'cv2.TM_CCOEFF_NORMED', threshold, save_rst)
#    print "is template_error.png in home.png? ", is_pattern_in_image('template_error.png', 'home.png', 'cv2.TM_CCOEFF_NORMED', threshold, save_rst)
#    print "is template_error.png in black.png? ", is_pattern_in_image('template_error.png', 'black.png', 'cv2.TM_CCOEFF_NORMED', threshold, save_rst)


