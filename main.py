import cv2
import numpy as np
import pyautogui
import os
from pynput import keyboard
import threading
import sys

# Function to load images from directory
def load_images_from_directory(directory):
    image_list = []
    for entry in os.scandir(directory):
        if entry.name.endswith(".jpg"):
            img = cv2.imread(os.path.join(directory, entry.name), cv2.IMREAD_GRAYSCALE)
            image_list.append((img))  # Store both name and image as a tuple
    return image_list


left_start = 300
top_start = 345

# Capture the screen within the specified region
def capture_screen(screen_width = 680, screen_height = 650):
    screen_region = (300, 345, screen_width, screen_height)
    screenshot = pyautogui.screenshot(region=screen_region)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

# Function to perform template matching and return matched locations
# def find_matched_regions(captured_image, template):
#     gray_frame = captured_image
#     result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
#     locations = np.where(result >= 0.8)
#     locations = list(zip(*locations[::-1]))
#     return locations
def find_matched_regions(frame, template):
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    # print(max_val)
    if max_val > .8:
        return max_loc
    else:
        return None

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
    currency_index = 0

    while running:

        frame = capture_screen()

        first_check = find_matched_regions(frame, currency_images[currency_index])
        if first_check is not None:
            # pyautogui.moveTo(first_check[0] + left_start + 2, first_check[1] + top_start + 2)

            # Draw a rectangle around the found item
            h, w = currency_images[currency_index].shape
            top_left = first_check
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 255), 2)
        else:
            currency_index += 1

        if currency_index >= len(currency_images):
            reroll_btn = find_matched_regions(frame, buttons_images[1])
            if reroll_btn is not None:
                pyautogui.moveTo(reroll_btn[0] + left_start + 12, reroll_btn[1] + top_start + 12, .2)
                pyautogui.click()
            else:
                print('No reroll')
                break
            currency_index = 0

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



