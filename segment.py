import cv2
import numpy as np
import os

def percent_green(mask):
    """Calculate the percentage of green pixels in the mask."""
    total_pixels = mask.size
    green_pixels = np.count_nonzero(mask)  # Count nonzero (white) pixels
    return (green_pixels / total_pixels) * 100

def detect_green_HSV(image_path):
    """Detect green color in an image using HSV segmentation and display results."""
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}. Check the file path.")
        return
    
    # Resize image for consistent display
    image = cv2.resize(image, (600, 400))
    
    # Convert to HSV color space
    HSV_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define HSV range for green
    lower_HSV_values = np.array([36, 50, 50], dtype='uint8')
    upper_HSV_values = np.array([86, 255, 255], dtype='uint8')
    
    # Create a mask where green areas are white and rest is black
    mask = cv2.inRange(HSV_image, lower_HSV_values, upper_HSV_values)
    
    # Calculate green percentage
    green_percentage = percent_green(mask)
    
    # Apply the mask to show only green regions
    segmented_output = cv2.bitwise_and(image, image, mask=mask)
    
    # Get the filename without extension (assumed to be the year)
    filename = os.path.splitext(os.path.basename(image_path))[0]
    year = filename  # Filename itself is the year (e.g., "2025")
    
    # Custom text with filename (year) and percentage of green area
    result_text = f"{green_percentage:.2f}% Forest Area in the year {filename}"
    
    # Add text to the segmented image
    cv2.putText(segmented_output, result_text, (1, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

    # Resize window for better visualization
    cv2.namedWindow("Final Segmented Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Final Segmented Image", 1920, 1080)

    # Display the final segmented image
    cv2.imshow("Final Segmented Image", segmented_output)
    
    print(result_text)
    
    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Specify the image file
image_path = "Images/2011.png"  # Change this to the actual file path
detect_green_HSV(image_path)
