#!/usr/bin/env python

import numpy as np
import cv2 as cv
import pickle
from os.path import exists
from urllib.request import urlopen

class parkingImage:
    parking_spots = []
    threshold = 10

    def getFile(self, my_file):
        return cv.imread(my_file, cv.IMREAD_GRAYSCALE)
    
    def setBaseline(self, inputfile):
        self.base = self.getFile(inputfile)

    def imgDiff(self, source):
        scale_percent = 100 # percent of original size

        img_name = 't1.jpg'
        img1 = cv.imread(img_name, cv.IMREAD_GRAYSCALE)
        img2 = cv.imread(img_name, cv.IMREAD_GRAYSCALE)
        img1 = cv.cvtColor(source, cv.COLOR_BGR2GRAY)
        width = int(img1.shape[1] * scale_percent / 100)
        height = int(img1.shape[0] * scale_percent / 100)
        dim = (width, height)
        img1 = cv.resize(img1, dim, interpolation = cv.INTER_AREA)
        img2 = cv.resize(img2, dim, interpolation = cv.INTER_AREA)
        img_b = source
        img_b = cv.resize(img_b, dim, interpolation = cv.INTER_AREA)

        mydiff = cv.subtract(img2, img1)

        if exists(img_name+'.spots'):
            with open(img_name+'.spots', 'rb') as f:
                # The protocol version used is detected automatically, so we do not
                # have to specify it.
                self.parking_spots = pickle.load(f)
                self.parking_spots = [ [int(y * scale_percent/50) for y in x] for x in self.parking_spots]
        else:
            while True:
                r = cv.selectROI('select roi', img1)
                if r == (0,0,0,0):   
                    with open(img_name+'.spots', 'wb') as f:
                        # Pickle the 'data' dictionary using the highest protocol available.
                        self.parking_spots = [ [int(y * 50/scale_percent) for y in x] for x in self.parking_spots]
                        pickle.dump(self.parking_spots, f, pickle.HIGHEST_PROTOCOL)
                    break
                self.parking_spots.append(r)
        
        img1 = cv.Canny(image=img1, threshold1=100, threshold2=200)
        cv.imshow('im1 edg', img1)
        img2 = cv.Canny(image=img2, threshold1=100, threshold2=200) 
        cv.imshow('im2 edg', img2)

        total_free_spots = 0

        for r in self.parking_spots:
            cropped1 = img1[int(r[1]):int(r[1]+r[3]), 
                        int(r[0]):int(r[0]+r[2])]
            avg_color1 = np.average(cropped1)
            cropped2 = img2[int(r[1]):int(r[1]+r[3]), 
                        int(r[0]):int(r[0]+r[2])]
            avg_color2 = np.average(cropped2)
            print(r)
            print(avg_color1)
            print(avg_color2)
            color = (0,255,0) # green if free
            if avg_color1 > self.threshold:
                color = (0,0,255) # red for taken
            else:
                total_free_spots += 1
            img_b = cv.rectangle(img_b, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), color, 2)
        img_b = cv.putText(img_b, 'Free spots: '+str(total_free_spots), (100,250), cv.FONT_HERSHEY_TRIPLEX, 1, (255,0,0))
        cv.imshow('nice mark', img_b)
        print('total free spots at Yona street: ' + str(total_free_spots))
        
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
    #pi.setBaseline('1.jpg')
    #pi.showBaseline()
    #pi.showDiff('2.jpg')
    #stream = urlopen('http://192.168.187.78:8081/camera/mjpeg?type=.mjpg')
    cap = cv.VideoCapture('http://192.168.187.78:8081/')
    while True:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #cv.imshow('frame', gray)
        pi.imgDiff(frame)
        if (cv.waitKey(30) >= 0):
            break

if __name__ == '__main__':
    print(__doc__)
    main()
    cv.waitKey(0)
    cv.destroyAllWindows()