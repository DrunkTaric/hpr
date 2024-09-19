def calculate(object):
    data = []
    for box in object.output:
        for box2 in object.output:
            if box.distance == 0:
                box.close_x, box.close_y = box2.close_x, box2.close_y
                box.close_h, box.close_w = box2.close_h, box2.close_w
                box.distance = box.Distance(box2)
            else:
                if box.distance > box.Distance(box2):
                    box.close_x, box.close_y = box2.close_x, box2.close_y
                    box.close_h, box.close_w = box2.close_h, box2.close_w
                    box.distance = box.Distance(box2)
        data.append(box.distance)
    if len(data) > 0:
        return round(sum(data) / len(data))
    return "?"