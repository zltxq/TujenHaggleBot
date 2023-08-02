import cv2
import numpy as np
import pyautogui
import os
from pynput import keyboard
import threading
import sys

# Function to load images from directory
def load_images_from_directory(directory):
    image_names = []
    image_list = []
    for entry in os.scandir(directory):
        if entry.name.endswith(".jpg"):
            image_names.append(entry.name)
            img = cv2.imread(os.path.join(directory, entry.name), cv2.IMREAD_GRAYSCALE)
            image_list.append((entry.name, img))  # Store both name and image as a tuple
    return image_list

# # Set up screen capture
# screen_height = 650
# capture_region = (300, 255, screen_width, screen_height)
screen_width = 680
screen_height = 650
capture_region = (300, 345, screen_width, screen_height)

# Load custom template images
buttons_path = "images/templates/buttons"
currency_path = "images/templates/currency"

buttons_images = load_images_from_directory(buttons_path)
currency_images = load_images_from_directory(currency_path)

# Initialize bot state and flag to keep track of the bot's running state
running = False

# Function to start the bot
def start_bot():
    global running
    print("Bot started.")
    running = True

    while running:
        # Capture the screen within the specified region
        screenshot = pyautogui.screenshot(region=capture_region)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for name, template in currency_images:
            h, w = template.shape

            # Perform template matching
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # Adjust the threshold based on your requirements
            loc = np.where(res >= threshold)

            if len(loc[0]) > 0:
                for pt in zip(*loc[::-1]):
                    # Draw rectangle around the matched region
                    cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                    # print((res[pt[1], pt[0]] + 1) * 50) # confidence% of matched item
                    # print(f"Matched template: {name}") # name of matched template
                    break
                    # Perform actions on the detected template (if needed)
                    # ... (code to interact with the detected template)

                # Break the loop after drawing rectangle for one template
                break

        # Display the frame with detected template
        cv2.imshow("Screen Stream", frame)

        # Check for hotkey press to stop the bot
        if not running:
            break

        cv2.waitKey(1)

    print("Bot stopped.")
    cv2.destroyAllWindows()

# Function to stop the bot
def stop_bot():
    global running
    running = False

# Function to handle keyboard events
def on_press(key):
    if key == keyboard.KeyCode(char='s'):
        if not running:
            threading.Thread(target=start_bot).start()
        else:
            print("Bot is already running.")
    elif key == keyboard.KeyCode(char='q'):
        if running:
            stop_bot()
        else:
            print("Bot is not running.")
    elif key == keyboard.KeyCode(char='x'):
        print("Exiting the program.")
        stop_bot()
        sys.exit(0)  # Gracefully exit the main file

# Function to listen for hotkey events
def listen_for_hotkey():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start the hotkey listener in a separate thread
keyboard_thread = threading.Thread(target=listen_for_hotkey)
keyboard_thread.start()
