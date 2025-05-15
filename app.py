import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

def percent_green(mask):
    total_pixels = mask.size
    green_pixels = np.count_nonzero(mask)
    return (green_pixels / total_pixels) * 100

def detect_green_HSV(image):
    HSV_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_HSV_values = np.array([25, 10, 10], dtype='uint8')
    upper_HSV_values = np.array([90, 255, 255], dtype='uint8')
    mask = cv2.inRange(HSV_image, lower_HSV_values, upper_HSV_values)
    green_percentage = percent_green(mask)
    segmented_output = cv2.bitwise_and(image, image, mask=mask)
    result_text = f"{green_percentage:.2f}% Forest Area"
    cv2.putText(segmented_output, result_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    return segmented_output, result_text

st.title("ForestMonitor WebApplication")

uploaded_file = st.file_uploader("Upload an image...", type=["png", "jpg", "jpeg"])

image = None
pil_image = None

if uploaded_file is not None:
    try:
        pil_image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(pil_image)
        image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        st.error(f"Failed to process the uploaded image: {e}")
else:
    try:
        sample_path = "sample_forest.jpg"  # Ensure this file is in the same folder
        pil_image = Image.open(sample_path).convert("RGB")
        image_np = np.array(pil_image)
        image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        st.info("No image uploaded. Using sample image.")
    except Exception as e:
        st.error("No image uploaded and failed to load sample image.")

# Process and display if valid image is available
if image is not None:
    st.subheader("Original Image")
    st.image(pil_image, use_container_width=True)

    segmented_output, result_text = detect_green_HSV(image)

    st.subheader("Green Area Segmented Output")
    segmented_rgb = cv2.cvtColor(segmented_output, cv2.COLOR_BGR2RGB)
    st.image(Image.fromarray(segmented_rgb), use_container_width=True)

    st.success(result_text)
