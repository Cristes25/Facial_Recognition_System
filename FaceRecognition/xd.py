import cv2

functions = dir(cv2)
for f in functions:
    if "face" in f:
        print (f)