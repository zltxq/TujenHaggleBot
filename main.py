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
    x_adjustment = random.uniform(3, 15)
    y_adjustment = random.uniform(3, 15)

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
def drag(x_offset, y_offset):
    # Generate random adjustments for x_offset and y_offset
    x_adjustment = random.uniform(-5, 7)
    y_adjustment = random.uniform(-34, 25)

    # Generate random duration within the specified range
    duration_range = (0.2, 0.23)
    duration = random.uniform(*duration_range)

    # Apply the random adjustments to the offsets
    x_offset += x_adjustment
    y_offset += y_adjustment

    # Perform the left-click and drag with randomized speed, acceleration, and duration
    pyautogui.drag(x_offset, y_offset, duration, button='left', tween=pyautogui.easeInOutQuad)

def inventory_perform_move():
    global click_event  # Add the 'global' statement to access the global variable
    # Define inventory properties
    num_rows = 5
    row_height = 53
    row_height_center = row_height // 2
    row_width = 598
    indent_from_above = 586
    left_indent = 1275
    duration1 = random.uniform(1.8, 2.3)
    duration2 = random.uniform(0.2, .4)

    pyautogui.moveTo(left_indent + random.uniform(10, 20), indent_from_above + row_height_center + random.uniform(-5, 8), duration2, pyautogui.easeInOutQuad)

    click_event.set()
    # Hold the 'Ctrl' key down and click on all cells
    pyautogui.keyDown('ctrl')
    for row in range(num_rows):
        pyautogui.moveTo(left_indent + row_width + random.uniform(-15, 15), indent_from_above + row_height_center + random.uniform(-5, 8), duration1, pyautogui.easeInOutQuad)
        indent_from_above += 53
        if row < num_rows - 1:
            pyautogui.moveTo(left_indent + random.uniform(-15, 15), indent_from_above + row_height_center + random.uniform(-5, 8), duration2, pyautogui.easeInOutQuad)
    # Release the 'Ctrl' key
    pyautogui.keyUp('ctrl')

def inventory_perform_click():
    # Define the interval between clicks (0.1 seconds)
    click_interval = random.uniform(0.0116, 0.0325)

    while True:
        # Wait until the click_event is set (inventory_perform_move() is done)
        click_event.wait()
        # Perform the click
        pyautogui.click()
        # Wait for the specified interval before the next click
        time.sleep(click_interval)

        # Check if the click_event is cleared (stop clicking if inventory_perform_move() is done)
        if not click_event.is_set():
            break

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
left_start = 290
top_start = 250

slider_index = buttons_names.index('slider.jpg')
confirm_index = buttons_names.index('confirm.jpg')
reroll_index = buttons_names.index('reroll.jpg')
stash_button_index = buttons_names.index('stash.jpg')
tujen_button_index = buttons_names.index('tujen.jpg')

# Function to stash items from the inventory
def stash_items():
    # Stash cell dimensions and spacing
    cell_width = 52
    cell_height = 53
    indent_top = 586
    indent_left = 1275

    # Number of rows and columns in the inventory
    num_rows = 5
    num_columns = 12

    # Hold the 'Ctrl' key down and click on all cells
    pyautogui.keyDown('ctrl')
    for row in range(num_rows):
        for column in range(num_columns):
            # Calculate the coordinates of the center of the cell with a random offset
            x_center = indent_left + column * cell_width + cell_width // 2 + random.randint(-7, 5)
            y_center = indent_top + row * cell_height + cell_height // 2 + random.randint(-3, 5)

            # Generate random duration within the range of 0.1 to 0.3 seconds
            duration = random.uniform(0.1, 0.15)

            # Move the cursor to the center of the cell with random duration
            pyautogui.moveTo(x_center, y_center, duration, pyautogui.easeInOutQuad)

            # Click on the cell without releasing the 'Ctrl' key
            pyautogui.click()

            # Generate a random interval between 0.01 to 0.03 seconds
            click_interval = random.uniform(0.003, 0.008)
            time.sleep(click_interval)

    # Release the 'Ctrl' key
    pyautogui.keyUp('ctrl')


# # Create a threading.Event object to control clicking
# click_event = threading.Event()


# Function to start the bot
print('Bot is ready, press "T" to begin, "Q" to pause and "X" to exit')
def start_bot():
    global running
    print("Bot started.")
    running = True
    currency_index = 0
    full_inventory_counter = 0

    while running:
        frame = capture_screen()

        # currency check
        currency_location = template_match(currency_images[currency_index])
        if currency_location is not None:
            # cv2.rectangle(frame, (currency_location[0], currency_location[1]),
            #               (currency_location[0] + 25, currency_location[1] + 25), (255, 255, 255), 2)
            move_cursor(currency_location[0], currency_location[1])
            left_click()

            slider_location = template_match(buttons_images[slider_index])
            if slider_location is not None:
                move_cursor(slider_location[0], slider_location[1])
                drag(-120, 0)

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

        # Reroll button
        if currency_index >= len(currency_images):
            reroll_location = template_match(buttons_images[reroll_index])
            if reroll_location is not None:
                move_cursor(reroll_location[0], reroll_location[1])
                time.sleep(random.uniform(0.3, 0.6))
                left_click()
            else:
                print('No reroll')
                # break

            currency_index = 0
            full_inventory_counter += 1

        # Put items to stash
        if full_inventory_counter >= 35:
            time.sleep(random.uniform(0.3, 0.5))
            # Press the 'Esc' key
            pyautogui.press('esc')


            stash_button_location = template_match(buttons_images[stash_button_index])
            if stash_button_location is not None:
                stash_x = stash_button_location[0] + left_start + random.uniform(3, 55)
                stash_y = stash_button_location[1] + top_start + random.uniform(2, 15)
                # stash_duration_range = (0.13, 0.2)
                stash_duration = random.uniform(0.2, 0.3)

                pyautogui.moveTo(stash_x, stash_y, stash_duration, pyautogui.easeInOutQuad)
                left_click()
                time.sleep(1)

                cell_width = 52
                cell_height = 53
                indent_top = 586
                indent_left = 1275

                # Number of rows and columns in the inventory
                num_rows = 5
                num_columns = 12

                # Hold the 'Ctrl' key down and click on all cells
                pyautogui.keyDown('ctrl')
                for row in range(num_rows):
                    if running:
                        for column in range(num_columns):
                            # Calculate the coordinates of the center of the cell with a random offset
                            x_center = indent_left + column * cell_width + cell_width // 2 + random.randint(-7, 5)
                            y_center = indent_top + row * cell_height + cell_height // 2 + random.randint(-3, 5)

                            # Generate random duration within the range of 0.1 to 0.3 seconds
                            duration = random.uniform(0.1, 0.15)

                            # Move the cursor to the center of the cell with random duration
                            pyautogui.moveTo(x_center, y_center, duration, pyautogui.easeInOutQuad)

                            # Click on the cell without releasing the 'Ctrl' key
                            pyautogui.click()

                            # Generate a random interval between 0.01 to 0.03 seconds
                            click_interval = random.uniform(0.003, 0.008)
                            time.sleep(click_interval)

                # Release the 'Ctrl' key
                pyautogui.keyUp('ctrl')
                full_inventory_counter = 0
                # Press the 'Esc' key
                pyautogui.press('esc')

                # Tujen find

                tujen_button_location = template_match(buttons_images[tujen_button_index])
                if tujen_button_location is not None:
                    tujen_x = tujen_button_location[0] + left_start + random.uniform(3, 180)
                    tujen_y = tujen_button_location[1] + top_start + random.uniform(2, 15)
                    tujen_duration = random.uniform(0.13, 0.2)

                    pyautogui.moveTo(tujen_x, tujen_y, tujen_duration, pyautogui.easeInOutQuad)
                    pyautogui.keyDown('ctrl')
                    left_click()
                    pyautogui.keyUp('ctrl')

                else:
                    print('Tujen not found')
                    break

            else:
                print('Stash button not found')
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
    if key == keyboard.KeyCode(char='t'):
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



