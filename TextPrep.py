import numpy as np
import cv2
from predictor import neural
import os
import csv
import gc
import concurrent.futures
from tkinter import messagebox
import time
csvfile='tocsv.csv'
newcsvfile='tocsv1.csv'
class ImgPrep:
    letters = []
    imgDS = []
    imgDSLetter = []
    imgDSLetterVal = []

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    shrinkValue = 1
    borderType = cv2.BORDER_CONSTANT
    def __init__(self):
        pass
    def imgShrink(self,int, img):
        height, width = img.shape
        imgShrinkHeight = 1 * height // 100
        imgShrinkWidth = 1 * width // 100
        img = img[imgShrinkHeight:height - imgShrinkHeight, imgShrinkWidth:width - imgShrinkWidth]
        return img



    def getVal(self,op):
        if (op == "0"):
            return 0
        elif (op == "1"):
            return 1
        elif (op == "2"):
            return 2
        elif (op == "3"):
            return 3
        elif (op == "4"):
            return 4
        elif (op == "5"):
            return 5
        elif (op == "6"):
            return 6
        elif (op == "7"):
            return 7
        elif (op == "8"):
            return 8
        elif (op == "9"):
            return 9
        elif (op == "A"):
            return 10
        elif (op == "B"):
            return 11
        elif (op == "C"):
            return 12
        elif (op == "D"):
            return 13
        elif (op == "E"):
            return 14
        elif (op == "F"):
            return 15
        elif (op == "G"):
            return 16
        elif (op == "H"):
            return 17
        elif (op == "I"):
            return 18
        elif (op == "J"):
            return 19
        elif (op == "K"):
            return 20
        elif (op == "L"):
            return "L"
        elif (op == "M"):
            return 21
        elif (op == "N"):
            return 22
        elif (op == "O"):
            return 23
        elif (op == "P"):
            return 24
        elif (op == "Q"):
            return 25
        elif (op == "R"):
            return 26
        elif (op == "S"):
            return 27
        elif (op == "T"):
            return 28
        elif (op == "U"):
            return 29
        elif (op == "V"):
            return 30
        elif (op == "W"):
            return 31
        elif (op == "X"):
            return 32
        elif (op == "Y"):
            return 33
        elif (op == "Z"):
            return 34
        elif (op == "a"):
            return 35
        elif (op == "b"):
            return 36
        elif (op == "d"):
            return 37
        elif (op == "e"):
            return 38
        elif (op == "f"):
            return 39
        elif (op == "g"):
            return 40
        elif (op == "h"):
            return 41
        elif (op == "n"):
            return 42
        elif (op == "q"):
            return 43
        elif (op == "r"):
            return 44
        elif (op == "t"):
            return 45
    def threshold(self,thresh, img):
        ret, img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
        return img


    def findLines(self,img):
        whiteHorizontal = []
        top = []
        bot = []
        imgArray = []
        height, width = img.shape

        for i in range(0, height):
            for j in range(0, width):
                if img[i, j] == 0:
                    break
                elif j == width - 1:
                    whiteHorizontal.append(i)
        for i in range(0, len(whiteHorizontal) - 1):
            if whiteHorizontal[i] + 1 != whiteHorizontal[i + 1]:
                top.append(whiteHorizontal[i])
                bot.append(whiteHorizontal[i + 1])
        for i in range(0, len(top)):
            temp = img[top[i]:bot[i], 0:width]
            imgArray.append(temp)

        return imgArray


    def findLetters(self,imgArray):
        letterArray = []
        for i in range(0, len(imgArray)):
            cropImg = imgArray[i]
            cHeight, cWidth = cropImg.shape
            whiteVertical = []
            left = []
            right = []
            for j in range(0, cWidth):
                for k in range(0, cHeight):
                    if cropImg[k, j] == 0:
                        break
                    elif k == cHeight - 1:
                        whiteVertical.append(j)

            for j in range(0, len(whiteVertical) - 1):
                if whiteVertical[j] + 1 != whiteVertical[j + 1]:
                    left.append(whiteVertical[j] + 1)
                    right.append(whiteVertical[j + 1])
            for j in range(0, len(left)):
                cropImg2 = cropImg[0:cHeight, left[j]:right[j]]
                letterArray.append(cropImg2)

        return letterArray


    def makeImgSquare(self,img):
        height, width = img.shape
        ratio = width / height
        if ratio < 1:
            img = cv2.copyMakeBorder(img, 0, 0, (height - width) // 2, (height - width) // 2, self.borderType, value=255)
        elif ratio > 1:
            img = cv2.copyMakeBorder(img, (width - height) // 2, (width - height) // 2, 0, 0, self.borderType, value=255)

        return img


    def removeWhiteSpace(self,img, axis):
        img = np.rot90(img, axis)
        height, width = img.shape
        temp1 = []
        temp2 = []
        for j in range(0, height):
            if not (np.sum(img[j]) == len(img[j]) * 255):
                temp1.append(img[j])
        temp1 = np.array(temp1)
        if axis != 0:
            temp1 = np.rot90(temp1, 3)
        return temp1


    def padImg(self,img, padx, pady, color):
        return cv2.copyMakeBorder(img, pady, pady, padx, padx, cv2.BORDER_CONSTANT, value=color)


    def formatImg(self,img):
        img = np.bitwise_not(img)  # switches the black and white pixels
        img = cv2.GaussianBlur(img, (1, 1), 0)
        img = cv2.resize(img, (28, 28), cv2.INTER_CUBIC)
        img = np.rot90(img, 3)
        img = cv2.flip(img, 2)
        return img


    def flattenImg(self,img):  # function for flattening image

        img = np.ravel(img)

        img.reshape(1, 784)

        return img

    def imageManip(self,img, degX, degY, rot):
        rows, cols = img.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rot, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        M = np.float32([[1,0, degX],[0,1,degY]])
        dst = cv2.warpAffine(dst, M, (cols,rows))
        return dst



    def seperateAnalyse(self,img):
        img = self.imgShrink(self.shrinkValue, img)

        textLines = self.findLines(img)
        letters = self.findLetters(textLines)

        for i in range(0, len(letters)):
            letters[i] = self.removeWhiteSpace(letters[i], 0)
            letters[i] = self.removeWhiteSpace(letters[i], 1)
            letters[i] = self.makeImgSquare(letters[i])
            letters[i] = self.padImg(letters[i], 4, 4, 255)
            letters[i] = self.formatImg(letters[i])

        return letters
    def func(self,img):
        transform = [-2, -1, 0, 1, 2]
        temp1 = img
        temp1 = self.formatImg(temp1)
        x = neural(temp1)
        y = self.getVal(x)
        for j in range(0, len(transform)):
            for k in range(0, len(transform)):
                for l in range(0, len(transform)):
                    temp = img
                    temp = cv2.bitwise_not(temp)
                    temp = self.imageManip(temp, j, k, l)
                    temp = cv2.bitwise_not(temp)
                    temp = self.formatImg(temp)
                    self.imgDS.append(temp)
                    self.imgDSLetter.append(x)
                    self.imgDSLetterVal.append(y)
    def seperate(self,img):
        img = self.imgShrink(self.shrinkValue, img)
        textLines = self.findLines(img)
        letters = self.findLetters(textLines)

        for i in range(0, len(letters)):
            letters[i] = self.removeWhiteSpace(letters[i], 0)
            letters[i] = self.removeWhiteSpace(letters[i], 1)
            letters[i] = self.makeImgSquare(letters[i])
            letters[i] = self.padImg(letters[i], 4, 4, 255)
            letters[i] = self.formatImg(letters[i])
        return letters
    def saveCsv(self, img, text):
        letters = self.seperate(img)
        print(text)
        s = ""
        print(len(letters))
        for i in range(0, len(letters)):
            tempImg =letters[i]
            x = neural(tempImg)
            print(x)

            #for i in range(0, len(letters)):

            tempImg = letters[i]
            flatImg = self.flattenImg(tempImg)
            with open(csvfile, "a") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow(flatImg)

            count = 0
        with open(csvfile, 'r') as csvinput:
            with open(newcsvfile, 'a') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                for row in csv.reader(csvinput):
                    writer.writerow([text] + row)

    val = ""
    def analyse(self, img):
        start = time.time()
        val = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 'A', 11: 'B', 12: 'C',
           13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N',
           24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y',
           35: 'Z', 36: 'a', 37: 'b', 38: 'd', 39: 'e', 40: 'f', 41: 'g', 42: 'h', 43: 'n', 44: 'q', 45: 'r', 46: 't'}
        a = self.seperateAnalyse(img)
        str1 = ""
        le = len(a)
        x = neural(a,le)
        #print("shape ",a.shape)
        for i in range(0, len(x)):
            out = val[x[i]]
            str1 = str1 + str(out)
        end = time.time()
        print("time ",end - start)
        return str1
