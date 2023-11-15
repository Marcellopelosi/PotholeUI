import streamlit as st
from PIL import Image
import pandas as pd

# Function to display selected image
def display_image(image_path):
    img = Image.open(image_path)
    st.image(img, caption='Selected Image', use_column_width=True)

st.markdown("### Upload a video file:")
uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi'])

if uploaded_file is not None:

    # Sample data for the table
    data = {
        'Image': ['Image 1', 'Image 2', 'Image 3'],
        'Path': ['path_to_image1.jpg', 'path_to_image1.jpg', 'path_to_image1.jpg']
    }
    df = pd.DataFrame(data)

    st.title('Image Selector App')

    # Display the table
    st.dataframe(df)

    # Selectbox to choose the image
    selected_frame = st.selectbox('Select Image', df['Path'])

    # Display the selected image
    display_image(selected_frame)
