import numpy as np
import cv2
from predictor import neural
import os
import gc
import sys

def findLines(img):
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
def findLetters(imgArray):
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
def removeWhiteSpace(img, axis):
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
def makeImgSquare(img):
	height, width = img.shape
	ratio = width / height
	if ratio < 1:
		img = cv2.copyMakeBorder(img, 0, 0, (height - width) // 2, (height - width) // 2, cv2.BORDER_CONSTANT, value=255)
	elif ratio > 1:
		img = cv2.copyMakeBorder(img, (width - height) // 2, (width - height) // 2, 0, 0, cv2.BORDER_CONSTANT, value=255)

	return img
def formatImg(img):
	img = np.bitwise_not(img)  # switches the black and white pixels
	img = cv2.GaussianBlur(img, (1, 1), 0)
	img = cv2.resize(img, (28, 28), cv2.INTER_CUBIC)
	img = np.rot90(img, 3)
	img = cv2.flip(img, 2)
	return img
	
	
	
imgName = sys.argv[1]
val = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 'A', 11: 'B', 12: 'C',
           13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N',
           24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y',
           35: 'Z', 36: 'a', 37: 'b', 38: 'd', 39: 'e', 40: 'f', 41: 'g', 42: 'h', 43: 'n', 44: 'q', 45: 'r', 46: 't'}
img = cv2.imread(imgName,0)
imgArray = findLines(img)
letters = findLetters(imgArray)
str1=""

for i in range(0, len(letters)):
	
	letters[i] = removeWhiteSpace(letters[i], 0)
	
	letters[i] = removeWhiteSpace(letters[i], 1)
	
	letters[i] = makeImgSquare(letters[i])
	
	letters[i] = cv2.copyMakeBorder(letters[i], 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=255)
	letters[i] = formatImg(letters[i])

x = neural(letters,len(letters))
for i in range(0, len(x)):
	out = val[x[i]]
	str1 = str1 + str(out)
	
print (str1)



