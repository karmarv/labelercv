from PIL import Image
from model_handler import ModelHandler

labels = { 0 : "rose"}
# Read the DL model
model = ModelHandler(labels)

# Read Image
image = Image.open("./DJI_0002.JPG")
threshold = 0.5
results = model.infer(image, threshold)
print(results)