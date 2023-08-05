import cv2
import numpy as np
import pyautogui
import os
from pynput import keyboard
import threading
import sys
import random
import time

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

# Function to move the cursor to a given location
def move_cursor(x, y, duration_range=(0.13, 0.2)):
    # Generate random values for cursor position adjustments
    x_adjustment = random.uniform(1, 15)
    y_adjustment = random.uniform(1, 15)

    # Generate random duration within the specified range
    duration = random.uniform(*duration_range)

    # Apply the random adjustments to the cursor position
    x += left_start + x_adjustment
    y += top_start + y_adjustment

    # Move the cursor with randomized speed and acceleration
    pyautogui.moveTo(x, y, duration, pyautogui.easeInOutQuad)

# Function to perform a left-click at the current cursor location with randomized interval
def left_click(click_interval_range=(0.02, 0.06)):
    # Generate random interval for the click
    click_interval = random.uniform(*click_interval_range)
    time.sleep(click_interval)

    # Perform the left-click + post click interval
    pyautogui.click()
    time.sleep(click_interval)

# Function to perform a left-click and drag at the current cursor location with randomized values
def drag(x_offset, y_offset, duration_range=(0.13, 0.2)):
    # Generate random adjustments for x_offset and y_offset
    x_adjustment = random.uniform(-10, 5)
    y_adjustment = random.uniform(-18, 24)

    # Generate random duration within the specified range
    duration = random.uniform(*duration_range)

    # Apply the random adjustments to the offsets
    x_offset += x_adjustment
    y_offset += y_adjustment

    # Perform the left-click and drag with randomized speed, acceleration, and duration
    pyautogui.drag(x_offset, y_offset, duration, button='left', tween=pyautogui.easeInOutQuad)

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
print('Bot is ready, press "S" to begin, "Q" to pause and "X" to exit')
def start_bot():
    global running
    print("Bot started.")
    running = True
    currency_index = 0

    while running:
        frame = capture_screen()
        # currency check
        currency_location = template_match(currency_images[currency_index])
        if currency_location is not None:
            move_cursor(currency_location[0], currency_location[1])
            left_click()

            slider_index = buttons_names.index('slider.jpg')
            slider_location = template_match(buttons_images[slider_index])
            if slider_location is not None:
                move_cursor(slider_location[0], slider_location[1])
                drag(-120, 0)

            confirm_index = buttons_names.index('confirm.jpg')
            confirm_location = template_match(buttons_images[confirm_index])
            move_cursor(confirm_location[0], confirm_location[1])
            left_click()

            # Check for slider and confirm again
            slider_location = template_match(buttons_images[slider_index])
            if slider_location is not None:
                move_cursor(slider_location[0], slider_location[1])
                drag(-55, 0)
                confirm_location = template_match(buttons_images[confirm_index])
                move_cursor(confirm_location[0], confirm_location[1])
                left_click()

                # Check for slider and confirm one more time
                slider_location = template_match(buttons_images[slider_index])
                if slider_location is not None:
                    confirm_location = template_match(buttons_images[confirm_index])
                    move_cursor(confirm_location[0], confirm_location[1])
                    left_click()
        else:
            currency_index += 1

        if currency_index >= len(currency_images):
            reroll_index = buttons_names.index('reroll.jpg')
            reroll_location = template_match(buttons_images[reroll_index])
            if reroll_location is not None:
                move_cursor(reroll_location[0], reroll_location[1])
                left_click()
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



