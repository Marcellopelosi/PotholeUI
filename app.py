import streamlit as st
from PIL import Image

# Sample data for the table
data = {
    'Image': ['Image 1', 'Image 2', 'Image 3'],
    'Path': ['path_to_image1.jpg', 'path_to_image1.jpg', 'path_to_image1.jpg']
}
df = pd.DataFrame(data)

# Function to display selected image
def display_image(image_path):
    img = Image.open(image_path)
    st.image(img, caption='Selected Image', use_column_width=True)

# Streamlit app
def main():
    st.title('Image Selector App')

    # Display the table
    st.table(df)

    # Selectbox to choose the image
    selected_image = st.selectbox('Select Image', df['Path'])

    # Display the selected image
    display_image(selected_image)

if __name__ == '__main__':
    main()
