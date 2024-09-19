import cv2

def calculate(object):#calculating trhe pen presure
    pp = 0.0 #pen preasure
    image = cv2.cvtColor(object.src_img.copy(), cv2.COLOR_BGR2GRAY)#importing + converting to grayscale first
    # inverting the image pixel by pixel individually. This costs the maximum time and processing in the entire process!
    h, w = object.src_gray.shape[:]
    inverted = object.src_gray 
    for x in range(h):
        for y in range(w):
            inverted[x][y] = 255 - image[x][y]
    filtered = cv2.bilateralFilter(inverted, 3, 50, 50) # adding bilateral filter
    # binary thresholding. Here we use 'threshold to zero' which is crucial for what we want.
    # If src(x,y) is lower than threshold=100, the new pixel value will be set to 0, else it will be left untouched!
    ret, thresh = cv2.threshold(filtered, 100, 255, cv2.THRESH_TOZERO)
    # add up all the non-zero pixel values in the image and divide by the number of them to find the average pixel value in the whole image
    total_intensity, pixel_count = 0, 0
    for x in range(h):
        for y in range(w):
            if(thresh[x][y] > 0):
                total_intensity += thresh[x][y]
                pixel_count += 1
    return round(float(total_intensity) / pixel_count)