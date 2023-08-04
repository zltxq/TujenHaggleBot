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
    image_names = []
    for entry in os.scandir(directory):
        if entry.name.endswith(".jpg"):
            img = cv2.imread(os.path.join(directory, entry.name), cv2.IMREAD_GRAYSCALE)
            image_list.append(img)
            image_names.append(entry.name)
    return image_list, image_names

# Capture the screen within the specified region
def capture_screen(screen_width = 680, screen_height = 650):
    screen_region = (left_start, top_start, screen_width, screen_height)
    screenshot = pyautogui.screenshot(region=screen_region)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame


def template_match(template):
    screen_img = capture_screen()
    result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    # print(max_val)
    if max_val > .8:
        return max_loc
    else:
        return None

# Load custom template images
buttons_path = "images/templates/buttons"
currency_path = "images/templates/currency"

currency_images = load_images_from_directory(currency_path)[0]
currency_names = load_images_from_directory(currency_path)[1]
buttons_images = load_images_from_directory(buttons_path)[0]
buttons_names = load_images_from_directory(buttons_path)[1]

# Initialize bot state and flag to keep track of the bot's running state
running = False

# margin left/top
left_start = 300
top_start = 345

# Function to start the bot
def start_bot():
    global running
    print("Bot started.")
    running = True
    currency_index = 0

    while running:
        frame = capture_screen()

        first_check = template_match(currency_images[currency_index])
        if first_check is not None:
            # pyautogui.moveTo(first_check[0] + left_start + 2, first_check[1] + top_start + 2)

            # Draw a rectangle around the found item
            h, w = currency_images[currency_index].shape
            top_left = first_check
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 255), 2)

            print(currency_names[currency_index])

        else:
            currency_index += 1

        if currency_index >= len(currency_images):
            index_btn = buttons_names.index('reroll.jpg')
            reroll_btn = template_match(buttons_images[index_btn])
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



