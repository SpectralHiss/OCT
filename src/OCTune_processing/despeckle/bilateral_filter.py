import cv2

def despeckle(image):
  return cv2.bilateralFilter(image,30,50,50)