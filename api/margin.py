import numpy as np

def horizontalProjection(img): #function to calculate horizontal projection of the image pixel rows and return it
    # Return a list containing the sum of the pixels in each row
    (h, w) = img.shape[:2]
    sumRows = []
    for j in range(h):
        row = img[j:j+1, 0:w] # y1:y2, x1:x2
        sumRows.append(np.sum(row))
    return sumRows

def calculate(object, Lsize):
    # extract a python list containing values of the horizontal projection of the image into 'hp'
    hpList = horizontalProjection(object.resized_thresh)
    # Extracting 'Top Margin' feature.
    topMarginCount = 0
    for sum in hpList:
        # sum can be strictly 0 as well. Anyway we take 0 and 255.
        if(sum<=255):
            topMarginCount += 1
        else:
            break
    if (Lsize == 0): Lsize = 1
    return float(topMarginCount) / Lsize