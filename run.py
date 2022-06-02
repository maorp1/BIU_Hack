#!/usr/bin/env python

import numpy as np
import cv2 as cv

class parkingImage:
    def getFile(self, my_file):
        return cv.imread(my_file, cv.IMREAD_GRAYSCALE)
    
    def setBaseline(self, inputfile):
        self.base = self.getFile(inputfile)

    def imgDiff(self, img1, img2):
        scale_percent = 50 # percent of original size

        img1 = cv.imread('parking1.jpg', cv.IMREAD_GRAYSCALE)
        img2 = cv.imread('parking1.jpg', cv.IMREAD_GRAYSCALE)
        width = int(img1.shape[1] * scale_percent / 100)
        height = int(img1.shape[0] * scale_percent / 100)
        dim = (width, height)
        img1 = cv.resize(img1, dim, interpolation = cv.INTER_AREA)
        img2 = cv.resize(img2, dim, interpolation = cv.INTER_AREA)

        mydiff = cv.subtract(img2, img1)

        r = cv.selectROI('select roi', img1)
        img1 = cv.Canny(image=img1, threshold1=100, threshold2=200)
        cv.imshow('im1 edg', img1)
        img2 = cv.Canny(image=img2, threshold1=100, threshold2=200) 
        cv.imshow('im2 edg', img2)
        cropped1 = img1[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        avg_color1 = np.average(cropped1)
        cropped2 = img2[int(r[1]):int(r[1]+r[3]), 
                      int(r[0]):int(r[0]+r[2])]
        avg_color2 = np.average(cropped2)
        print(avg_color1)
        print(avg_color2)
        
        return cv.subtract(img2, img1)

    def scanAllROI(self):
        print('TODO')
    
    def addROI(self):
        print('TODO')
        
    def showBaseline(self):
        cv.imshow('baseline', self.base)
    
    def showDiff(self, img):
        mydiff = self.imgDiff(self.base, img)
        #cv.imshow('base diff', mydiff)

def main():
    pi = parkingImage()
    pi.setBaseline('1.jpg')
    pi.showBaseline()
    pi.showDiff('2.jpg')

if __name__ == '__main__':
    print(__doc__)
    main()
    cv.waitKey(0)
    cv.destroyAllWindows()