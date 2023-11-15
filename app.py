import streamlit as st
from PIL import Image
import pandas as pd
from Fundamentals import results_elaborator

model_path = "/best_pothole.pt"
video_path = "/temp_video.mp4"

# Function to display selected image
def display_image(image_path):
    img = Image.open(image_path)
    st.image(img, caption='Selected Image', use_column_width=True)

st.markdown("### Upload a video file:")
uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi'])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    results = results_elaborator(model_path, video_path)

    st.title('Image Selector App')

    # Display the table
    st.dataframe(results)

    # Selectbox to choose the image
    selected_frame = st.selectbox('Select Image', results["frame_number"].to_list())

    # Display the selected image
    display_image("/frame/" + selected_frame + ".jpg")
