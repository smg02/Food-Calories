from dotenv import load_dotenv

load_dotenv()  # Load all environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini API and get a response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
    response = model.generate_content([input_text, image, prompt])
    return response.text

# Function to prepare the image for AI processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = {
            "mime_type": uploaded_file.type,  # Get the MIME type
            "data": bytes_data
        }
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Health Advisor LIM App")

st.header("Health Advisor")
input_text = st.text_input("Input Prompt (if you need to mention anything specifically): ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)  # Updated parameter

# Submit button
submit = st.button("Tell me the total calories")

input_prompt = """
You are a nutritionist expert. Analyze the food items in the image and calculate the total calories.
Provide details for each food item in the following format:

1. Item 1 - X calories
2. Item 2 - Y calories
...
Finally, indicate whether the food is healthy and provide the percentage split of 
carbohydrates, fats, fiber, sugar, and other essential nutrients.
"""

# Process when the button is clicked
if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("Your Food Contains")
    st.write(response)
elif submit and uploaded_file is None:
    st.error("Please upload an image first!")
