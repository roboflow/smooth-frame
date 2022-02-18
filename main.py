from roboflow import Roboflow
import glob
from PIL import Image
import collections

from smooth import smooth

## INITIALZIATIONS
# ROBOFLOW
rf = Roboflow(api_key="YOUR_API_KEY")

# access the workspace object
workspace = rf.workspace()

# project, version, and inference model
project = workspace.project("YOUR_PROJECT_NAME")
version = project.version(1)
model = version.model

## EXECUTION
# CASE 1 - one object of specified class present (moving or static)
queue = collections.deque()
local_max = ["name", 0, "last_box", "x", "y"]
lookup_dict = {"empty": 0}

# get predictions from image
images = sorted(glob.glob('./test_images/*.png'))
for image in images:
    # open image using PIL
    img = Image.open(image)

    # get predictions from Roboflow CV
    predictions = model.predict(image)

    # render smoothly
    queue, local_max, lookup_dict = smooth(img, queue, local_max, lookup_dict, predictions)
       
# CASE 2 - multiple objects of same class present (targets always static)

