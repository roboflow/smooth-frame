from PIL import ImageDraw

def draw_boxes(box, x0, y0, img, class_name):
    # get position coordinates
    if(not class_name):
        return img

    bbox = ImageDraw.Draw(img) 

    bbox.rectangle(box, outline="green")
    bbox.text((x0, y0), class_name, fill='black', anchor='mm')

    return img

def smooth(img, queue, local_max, lookup_dict, predictions): 
    # params:
    # -- img (PIL Image) : image to render
    # -- queue (Collections Deque) : data structure for the sliding window
    # -- local_max (List) - contains name, box, and count for most present class in queue
    # -- lookup_dict (Dict) - contains counts of all values in queue
    # -- predictions (List[Dict]) - detected objects supplied by Roboflow CV
    
    current_frame = predictions.json()['predictions']

    # add detection or empty if no detections
    if current_frame and len(current_frame) > 0:
        # image to draw on

        # class name for rendering and tracking
        class_name = current_frame[0]['class']

        # bounding box for current prediction
        x0 = current_frame[0]['x'] - current_frame[0]['width'] / 2
        x1 = current_frame[0]['x'] + current_frame[0]['width'] / 2
        y0 = current_frame[0]['y'] - current_frame[0]['height'] / 2
        y1 = current_frame[0]['y'] + current_frame[0]['height'] / 2
        box = (x0, y0, x1, y1)

        # append to front of queue
        queue.appendleft(class_name)
        
        # add to look up
        if class_name in lookup_dict:
            lookup_dict[class_name] += 1
        else:
            lookup_dict[class_name] = 1

        # update local max name and value
        if lookup_dict[class_name] >= local_max[1]:
            local_max[0] = class_name
            local_max[1] = lookup_dict[class_name]
            local_max[2] = box
            local_max[3] = x0
            local_max[4] = y0

    else:
        queue.appendleft("empty")
        lookup_dict["empty"] += 1

        # update local max name and value
        if lookup_dict["empty"] >= local_max[1]:
            local_max[0] = "empty"
            local_max[1] = lookup_dict["empty"]
            local_max[2] = (0,0,0,0)
            local_max[3] = 0
            local_max[4] = 0

    # keep queue to length 5
    if len(queue) > 5:
        popped = queue.pop()

        # subtract from lookup
        lookup_dict[popped] -= 1

        # update local max value
        if local_max[0] == popped:
            local_max[1] -= 1

    print(queue, lookup_dict, local_max)
    
    if len(queue) >= 3:
       print("CLASS NAME == ", local_max[0])
       new_img = draw_boxes(local_max[2], local_max[3], local_max[4], img, local_max[0])
       new_img.show()
    else:
        # show something while we wait?
        img.show()

    return queue, local_max, lookup_dict
