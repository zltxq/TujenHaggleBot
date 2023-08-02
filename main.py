import cv2
import numpy as np
import pyautogui
import os

# test fo github
def load_images_from_directory(directory):
    image_names = []
    image_list = []
    for entry in os.scandir(directory):
        if entry.name.endswith(".jpg"):
            image_names.append(entry.name)
    for name in image_names:
        img = cv2.imread(os.path.join(directory, name), cv2.IMREAD_GRAYSCALE)
        image_list.append(img)
    return image_list

# Load custom template images
buttons_path = "images/templates/buttons"
currency_path = "images/templates/currency"

# Load the template images from the directories
buttons_images = load_images_from_directory(buttons_path)
currency_images = load_images_from_directory(currency_path)

# # Set up screen capture
# screen_height = 650
# capture_region = (300, 255, screen_width, screen_height)
screen_width = 680
screen_height = 650
capture_region = (300, 345, screen_width, screen_height)


while True:
    # Capture the screen within the specified region
    screenshot = pyautogui.screenshot(region=capture_region)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for template in currency_images:
        h, w = template.shape

        # Perform template matching
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust the threshold based on your requirements
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            for pt in list(zip(*loc[::-1])):
                # Draw rectangle around the matched region
                cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                break
                # Perform actions on the detected template (if needed)
                # ... (code to interact with the detected template)
            # Break the loop after drawing rectangle for one template
            break

    # Display the frame with detected template
    cv2.imshow("Screen Stream", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()