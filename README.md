# Smooth out flickering bounding boxes

## How to use smooth

Call `smooth()` with the following parameters:

### params:
- img (PIL Image) : image to render
- queue (Collections Deque) : data structure for the sliding window
- local_max (List) - contains name, box, and count for most present class in queue
- lookup_dict (Dict) - contains counts of all values in queue
- predictions (List[Dict]) - detected objects supplied by Roboflow CV

