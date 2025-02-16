import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
from datetime import datetime
import random
import pyautogui
import json
from selenium.webdriver.common.action_chains import ActionChains
from evpn import ExpressVpnApi
import string
pyautogui.FAILSAFE = False
current_time = int(datetime.now().timestamp())
random.seed(current_time)

class FillWebsite:
    def __init__(self):
       pass
        
    def is_element_present(self,driver,locator_type, locator_value, timeout=10):
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator_value))
            )
            return True
        except:
            return False
    def type_slowly(self,element, text, delay_range=(0.3, 0.5)):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))  # Random delay between each keystroke
    # Main function to iterate over rows in the Excel file

        
    def log_error(self,row, log_file='error_log.txt'):
        with open(log_file, 'a+') as f:
            forename = row.get('forename', 'N/A')  # Get forename from row, default to 'N/A' if not present
            surname = row.get('surname', 'N/A')  # Get surname from row, default to 'N/A' if not present
            email = row.get('email_address', 'N/A')  # Get surname from row, default to 'N/A' if not present
            f.write(f"Error processing row: forename={forename}, surname={surname}, email = {email}\n")


        
    def move_and_click(self,driver, target, view=True):
        if(view == True):
            driver.execute_script("arguments[0].scrollIntoView(true);", target)
        element_rect = driver.execute_script(
            "var rect = arguments[0].getBoundingClientRect();"
            "return {x: rect.left, y: rect.top, width: rect.width, height: rect.height};",
            target
        )
        window_position = driver.get_window_position()
        window_x = window_position['x']
        window_y = window_position['y']

        # Calculate the coordinates relative to the screen
        start_x, start_y = pyautogui.position()  # Starting position of the mouse
        target_x = window_x + element_rect['x'] + element_rect['width'] / 2
        target_y = window_y + element_rect['y'] + element_rect['height'] / 2 + 100

        # Move the mouse smoothly to the target position
        self.move_mouse_smoothly(start_x, start_y, target_x, target_y, duration=random.uniform(0.5, 1.0))

        actions = ActionChains(driver)
        actions.move_to_element(target).click().perform()


        
    def move_mouse_smoothly(self,x1, y1, x2, y2, duration=1.0):
        """Move the mouse smoothly between two points using random intermediate steps."""
        # Number of steps to take
        num_steps = random.randint(10, 20)
        # Calculate the total time for each step
        step_duration = duration / num_steps
        
        # Random curve offset for more human-like movement
        random_curve_x = random.uniform(0.2, 0.8)
        random_curve_y = random.uniform(0.2, 0.8)

        for t in range(num_steps + 1):
            # Use t normalized between 0 and 1
            t = t / num_steps
            # Calculate intermediate points using random offsets
            intermediate_x = (1 - t) * x1 + t * x2 + random_curve_x * (random.random() - 0.5)
            intermediate_y = (1 - t) * y1 + t * y2 + random_curve_y * (random.random() - 0.5)
            
            # Move the mouse to this intermediate point
            pyautogui.moveTo(intermediate_x, intermediate_y)
            
            # Add a slight random sleep between movements to simulate more human behavior
            time.sleep(random.uniform(step_duration / 2, step_duration))

 
    def setup_driver(self):
        # global chrome_driver_path

        # service = Service(executable_path=chrome_driver_path)

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("debuggerAddress", debugger_address)
        user_agent = UserAgent().random  # Random User-Agent for the session
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"user-agent={user_agent}")


        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    
        print(f"driver setup finished")
        return driver
        

    
    def generate_strong_password(self,length=8):
        if length < 8:
            raise ValueError("Password length should be at least 8 characters")

        # Define the required characters
        lower = string.ascii_lowercase  # a-z
        upper = string.ascii_uppercase  # A-Z
        digits = string.digits          # 0-9
        all_chars = lower + upper + digits
        
        # Ensure at least one upper case letter and one digit
        password = [
            random.choice(upper),   # At least one upper case letter
            random.choice(digits)   # At least one digit
        ]

        # Fill the rest of the password with random characters
        password += random.choices(all_chars, k=length - 2)

        # Shuffle to ensure randomness
        random.shuffle(password)
        
        return ''.join(password)

        