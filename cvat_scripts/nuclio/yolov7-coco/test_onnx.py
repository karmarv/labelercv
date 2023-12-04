from PIL import Image
from model_handler import ModelHandler

labels = { 0 : "person"}
# Read the DL model
model = ModelHandler(labels)

# Read Image
image = Image.open("./park_people.jpg")
threshold = 0.5
results = model.infer(image, threshold)
print(results)