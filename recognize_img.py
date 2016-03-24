import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import matplotlib.pyplot as plt


def recognize(image_path):
    clf1 = joblib.load("digits_svn.pkl")
    clf2 = joblib.load("digits_rf.pkl")
    
    im = cv2.imread(image_path)

    
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

    
    im_gray = cv2.adaptiveThreshold(im_gray, im_gray.mean(), 1, 1, 11, 2)

    
    ctrs, hier = cv2.findContours(im_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    
    rects = []
    for ctr in ctrs:
        if cv2.contourArea(ctr) > 200:
            [x, y, w, h] = cv2.boundingRect(ctr)
            if min(h, w) * 4 > max(h, w):
                rects.append([x, y, w, h])
                # rects = [cv2.boundingRect(ctr) for ctr in ctrs]

    
    for rect in rects:
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
        
        leng = int(rect[3] * 1.6)
        pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
        pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
        roi = im_gray[pt1:pt1 + leng, pt2:pt2 + leng]
        if roi.size > 0:
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
            nbr1 = clf1.predict(np.array([roi_hog_fd], 'float64'))
            nbr2 = clf2.predict(np.array([roi_hog_fd], 'float64'))
            answ = "s:" + str(int(nbr1[0])) + ",f:" + str(int(nbr2[0]))
            cv2.putText(im, answ, (rect[0], rect[1]), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1)

    cv2.imwrite(image_path,im)
    
