import cv2
import math
import numpy as np

def calculate(object):
    dst = cv2.Canny(object.src_img.copy(), 50, 200, None, 3)
    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 100, None, 50, 10)
    if linesP is not None:
        data = []
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
            angle = math.atan2(l[1]- l[3], l[0] - l[1])
            data.append(angle * 180 / np.pi)
        return round(sum(data) / len(data), 2)   
    return 0.0