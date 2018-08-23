import cv2

def despeckle(image):
  return cv2.bilateralFilter(image,20,20,15)