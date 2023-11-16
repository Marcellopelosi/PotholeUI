import streamlit as st
from PIL import Image
import torch

# Load an image from file or URL
image = Image.open("path_to_image1.jpg")  # Replace "path_to_your_image.jpg" with your image file's path

# Display the image
st.image(image, caption='Your Image', use_column_width=True)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Image
im = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(im)

st.markdown(results.pandas().xyxy[0])
