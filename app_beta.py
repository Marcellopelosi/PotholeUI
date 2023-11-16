import streamlit as st
from PIL import Image

# Load an image from file or URL
image = Image.open("path_to_image1.jpg")  # Replace "path_to_your_image.jpg" with your image file's path

# Display the image
st.image(image, caption='Your Image', use_column_width=True)
