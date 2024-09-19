import numpy as np

def horizontalProjection(img): #function to calculate horizontal projection of the image pixel rows and return it
    # Return a list containing the sum of the pixels in each row
    (h, w) = img.shape[:2]
    sumRows = []
    for j in range(h):
        row = img[j:j+1, 0:w] # y1:y2, x1:x2
        sumRows.append(np.sum(row))
    return sumRows

def calculate(object):
    lines = [] # a 2D list storing the vertical start index and end index of each contour
    space_zero = [] # stores the amount of space between lines
    # FIRST we extract the straightened contours from the image by looking at occurance of 0's in the horizontal projection.
    lineTop = 0
    lineBottom = 0
    spaceTop = 0
    spaceBottom = 0
    indexCount = 0
    setLineTop = True
    setSpaceTop = True
    includeNextSpace = True
    # extract a python list containing values of the horizontal projection of the image into 'hp'
    hpList = horizontalProjection(object.resized_thresh)
    # we are scanning the whole horizontal projection now
    for i, sum in enumerate(hpList):
            # sum being 0 means blank space
        if(sum==0):
            if(setSpaceTop):
                spaceTop = indexCount
                setSpaceTop = False # spaceTop will be set once for each start of a space between lines
            indexCount += 1
            spaceBottom = indexCount
            if(i<len(hpList)-1): # this condition is necessary to avoid array index out of bound error
                if(hpList[i+1]==0): # if the next horizontal projectin is 0, keep on counting, it's still in blank space
                    continue
            # we are using this condition if the previous contour is very thin and possibly not a line
            if(includeNextSpace):
                space_zero.append(spaceBottom-spaceTop)
            else:
                if (len(space_zero)==0):
                    previous = 0
                else:
                    previous = space_zero.pop()
                space_zero.append(previous + spaceBottom-lineTop)
            setSpaceTop = True # next time we encounter 0, it's begining of another space so we set new spaceTop
        # sum greater than 0 means contour
        if(sum>0):
            if(setLineTop):
                lineTop = indexCount
                setLineTop = False # lineTop will be set once for each start of a new line/contour
            indexCount += 1
            lineBottom = indexCount
            if(i<len(hpList)-1): # this condition is necessary to avoid array index out of bound error
                if(hpList[i+1]>0): # if the next horizontal projectin is > 0, keep on counting, it's still in contour
                    continue
                # if the line/contour is too thin <10 pixels (arbitrary) in height, we ignore it.
                # Also, we add the space following this and this contour itself to the previous space to form a bigger space: spaceBottom-lineTop.
                if(lineBottom-lineTop<20):
                    includeNextSpace = False
                    setLineTop = True # next time we encounter value > 0, it's begining of another line/contour so we set new lineTop
                    continue
            includeNextSpace = True # the line/contour is accepted, new space following it will be accepted
            # append the top and bottom horizontal indices of the line/contour in 'lines'
            lines.append([lineTop, lineBottom])
            setLineTop = True # next time we encounter value > 0, it's begining of another line/contour so we set new lineTop
    # SECOND we extract the very individual lines from the lines/contours we extracted above.
    fineLines = [] # a 2D list storing the horizontal start index and end index of each individual line
    for i, line in enumerate(lines):
        anchor = line[0] # 'anchor' will locate the horizontal indices where horizontal projection is > ANCHOR_POINT for uphill or < ANCHOR_POINT for downhill(ANCHOR_POINT is arbitrary yet suitable!)
        anchorPoints = [] # python list where the indices obtained by 'anchor' will be stored
        upHill = True # it implies that we expect to find the start of an individual line (vertically), climbing up the histogram
        downHill = False # it implies that we expect to find the end of an individual line (vertically), climbing down the histogram
        segment = hpList[line[0]:line[1]] # we put the region of interest of the horizontal projection of each contour here
        for j, sum in enumerate(segment):
            if(upHill):
                if(sum<6000):
                    anchor += 1
                    continue
                anchorPoints.append(anchor)
                upHill = False
                downHill = True
            if(downHill):
                if(sum>6000):
                    anchor += 1
                    continue
                anchorPoints.append(anchor)
                downHill = False
                upHill = True
        # we can ignore the contour here
        if(len(anchorPoints)<2):
            continue
        # len(anchorPoints) > 3 meaning contour composed of multiple lines
        lineTop = line[0]
        for x in range(1, len(anchorPoints)-1, 2):
            # 'lineMid' is the horizontal index where the segmentation will be done
            lineMid = (anchorPoints[x]+anchorPoints[x+1])/2
            lineBottom = lineMid
            # line having height of pixels <20 is considered defects, so we just ignore it
            # this is a weakness of the algorithm to extract lines (anchor value is ANCHOR_POINT, see for different values!)
            if(lineBottom-lineTop < 20):
                continue
            fineLines.append([lineTop, lineBottom])
            lineTop = lineBottom
        if(line[1]-lineTop < 20):
            continue
        fineLines.append([lineTop, line[1]])
    midzone_row_count = 0
    lines_having_midzone_count = 0
    for i, line in enumerate(fineLines):
        segment = hpList[int(line[0]):int(line[1])]
        for j, sum in enumerate(segment):
            if(not sum<15000):
                midzone_row_count += 1
                lines_having_midzone_count += 1
    # error prevention ^-^
    if(lines_having_midzone_count == 0): lines_having_midzone_count = 1
    # the number of spaces is 1 less than number of lines but total_space_row_count contains the top and bottom spaces of the line
    average_letter_size = float(midzone_row_count) / lines_having_midzone_count
    # letter size is actually height of the letter and we are not considering width
    return average_letter_size