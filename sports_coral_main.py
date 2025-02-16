import pandas as pd
from selenium import webdriver
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
def generate_strong_password(length=8):
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

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    # URL of the proxy list
with open('url.txt', 'r') as file:
    landing_url = file.read().strip()
user_password= "Jason1234!"

locations = config['locations']

# Load the Excel file
file_path = 'data.xlsx'  # Path to your Excel file

chrome_driver_path = "C:\\Users\\User1\\Documents\\Cors bot\\chromedriver-win64\\chromedriver.exe"
data = pd.read_excel(file_path)




# Function to set up the Selenium WebDriver with proxy
def setup_driver():
    global chrome_driver_path

    service = Service(executable_path=chrome_driver_path)

    chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    
    user_agent = UserAgent().random  # Random User-Agent for the session
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")


    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

   
    print(f"driver setup finished")
    return driver
    

# Function to click the Continue button
def click_continue_button(driver,step):
    print(f"click_continue_button_started")
    try:
        continueButton = driver.find_element(By.XPATH, f"(//button[@id='continue'])[{step}]")
        move_and_click(driver, continueButton)
        time.sleep(random.uniform(0.5, 0.1))
        print(f"click_continue_button_finished")
    except Exception as e:
        print(f"Error clicking the continue button: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

# Function to fill out the initial form
def fill_initial_form(driver, row):
    global user_password
    print(f"fill_initial_form started")
    try:
        # Navigate to the registration page
        driver.maximize_window()
        driver.get(landing_url)  # Replace with the actual URL
        join_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Join')]"))
        )
        time.sleep(random.uniform(2.0, 3.0))
        # Click the button
        move_and_click(driver, join_button)
        print("Join button clicked successfully")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "emailaddress"))
        )
        

        # Fill in the initial form fields
        phone_last_three = str(row['Telephone']).split(".")[0][:3]  # Get the last three digits of the telephone number
        user_id = f"{row['forename']}{row['surname']}{phone_last_three}"
        user_id = user_id.replace(" ", "")
        user_id = user_id.replace("'", "")
        user_id = user_id.lower()
        email_input = driver.find_element(By.NAME, "emailaddress")
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.ID, "focusPassword")
        user_password = generate_strong_password(random.randint(8, 13))
        
        pyautogui.click()  # Perform the click
        time.sleep(random.uniform(1,2))
        move_and_click(driver, email_input)
        # email_input.click()
        time.sleep(random.uniform(0.1, 0.3))
        move_and_click(driver, username_input)
        time.sleep(random.uniform(0.1, 0.3))
        move_and_click(driver, password_input)
        time.sleep(random.uniform(0.1, 0.3))

        move_and_click(driver, email_input)
        type_slowly(email_input, row['email_address'].replace(" ", ""))
        # email_input.send_keys(Keys.RETURN)
        print(f"emailaddress filled as '{row['email_address']}'")
        time.sleep(random.uniform(0.5, 1.5))

        move_and_click(driver, username_input)
        type_slowly(username_input, user_id)
        # username_input.send_keys(Keys.RETURN)
        print(f"username filled")

        
        
        time.sleep(random.uniform(0.5, 1.5))
        move_and_click(driver, password_input)
 
        
        type_slowly(password_input, user_password)
        print(f"password filled")
        time.sleep(random.uniform(0.5, 1.5))

        
        move_and_click(driver, username_input)
        time.sleep(random.uniform(0.5, 1.5))
        move_and_click(driver, password_input)
        time.sleep(random.uniform(0.5, 1.5))
        # email_input.click()
        move_and_click(driver, email_input)
        time.sleep(random.uniform(0.5, 1.5))
        move_and_click(driver, username_input)
        continue_button_1_clickable = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "(//button[@id='continue'])[1]")))
        time.sleep(random.uniform(0.5, 1.0))
        
        click_continue_button(driver,1)
        print(f"fill_initial_form finished")
        time.sleep(2.5)
    except Exception as e:
        print(f"Error filling initial form for {row['forename']} {row['surname']}: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

def move_mouse_smoothly(x1, y1, x2, y2, duration=1.0):
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

# Function to fill out the additional details
def move_and_click(driver, target, view=True):
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
    move_mouse_smoothly(start_x, start_y, target_x, target_y, duration=random.uniform(0.5, 1.0))

    actions = ActionChains(driver)
    actions.move_to_element(target).click().perform()


def select_gender(driver, gender, row):
    print(f"select_gender_started")
    try:
        if gender.lower() == "mr":
            male_label = driver.find_element(By.XPATH, "//label[@for='Male']")
            move_and_click(driver, male_label)

        elif gender.lower() == "ms":
            female_label = driver.find_element(By.XPATH, "//label[@for='Female']")
            move_and_click(driver, female_label)

        else:
            male_label = driver.find_element(By.XPATH, "//label[@for='Male']")
            move_and_click(driver, male_label)
            
        print(f"select_gender_finished")
    except Exception as e:
        print(f"Error selecting gender: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

def fill_additional_details_1(driver, row):
    print(f"fill_additional_details_1_started")
    try:
        select_gender(driver, row['title'],row)
        firstname = driver.find_element(By.NAME, "firstname")
        lastname = driver.find_element(By.NAME, "lastname")
        move_and_click(driver, firstname)
        type_slowly(firstname, row['forename'])

        move_and_click(driver, lastname)
        type_slowly(lastname, row['surname'])

        date_of_birth = pd.to_datetime(row['date_of_birth'])

        dayElement = driver.find_element(By.NAME, "day")
        type_slowly(dayElement, str(date_of_birth.day))
        move_and_click(driver,dayElement)

        monthElement = driver.find_element(By.NAME, "month")
        type_slowly(monthElement, str(date_of_birth.month))
        move_and_click(driver,monthElement)
        
        yearElement=driver.find_element(By.NAME, "year")
        type_slowly(yearElement, str(date_of_birth.year))
        move_and_click(driver,yearElement)

        
        click_continue_button(driver,2)
        
        print(f"fill_additional_details_1_finished")
    except Exception as e:
        print(f"Error filling additional details1: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

def click_enter_address_manually(driver, row):

    try:
        print(f"click_enter_address_manually_started")
        enter_address_link = driver.find_element(By.LINK_TEXT, "Enter address manually")
        move_and_click(driver, enter_address_link)

        time.sleep(random.uniform(0.5, 1.0))  # Optional: Wait for the next step to load
        print(f"click_enter_address_manually_finished")
    except Exception as e:
        print(f"Error clicking the 'Enter address manually' link: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling
        
def toggle_select_all_promotion_options(driver,row):
    print(f"toggle_select_all_promotion_options_started")
    try:
        # Wait until the checkbox is clickable
        checkbox_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='Email']")))
        move_and_click(driver, checkbox_label)
        # checkbox_label.click()  # Click to select the checkbox
        print("Checkbox 'Select All Promotion Options' is now checked.")

        print(f"toggle_select_all_promotion_options_started")
    except Exception as e:
        print(f"Error toggling the checkbox: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

def click_create_account_button(driver,row):
    print(f"click_create_account_button_started")
    try:
        time.sleep(1)
        
        submit_button = driver.find_element(By.ID, "submit")
        
        # actions = ActionChains(driver)

        # actions.move_to_element(submit_button).pause(random.uniform(0.5, 1.0)).perform()
        move_and_click(driver, submit_button)
        print("Successfully clicked the 'Create my account' button.")

        print(f"click_create_account_button_finished")
    except Exception as e:
        print(f"Error clicking the 'Create my account' button: {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

def fill_additional_details_2(driver, row):
    print(f"fill_additional_details_2_started")
    try:
        phone_input = driver.find_element(By.NAME, "mobilenumber")
        move_and_click(driver, phone_input)
        type_slowly(phone_input, str(row['Telephone']).split(".")[0])
        
        click_enter_address_manually(driver, row)
        house_number = row['House_Number']
        house_number_len = len(str(house_number).split(".")[0])
        print(house_number)
        address = ""
        if(house_number_len <= 3):
            print("left style")
            address =str(row['ad1'])
            print("qweqweqweqweqweqweqweqweqweqwqweqwe")
            if type(row['ad2']) == str:
                address += ', ' + row['ad2']
        else:
            print("right style")
            address =str(house_number)
            print("asdfsdfsdfadsfsadfsdfsadsdfa")
            if(type(row['ad1'])) == str:
                address += ', ' + row['ad1']
        print(address)
        address_input = driver.find_element(By.NAME, "addressline1")
        move_and_click(driver, address_input, False)

        type_slowly(address_input, address)

        city_input = driver.find_element(By.NAME, "addresscity")
        move_and_click(driver, city_input, False)
        type_slowly(city_input, row['ad4'])

        zip_input = driver.find_element(By.NAME, "addresszip")
        move_and_click(driver, zip_input,False)
        type_slowly(zip_input, row['postcode'])


        toggle_select_all_promotion_options(driver, row)
        time.sleep(random.uniform(1.0, 3.0))
        click_create_account_button(driver, row)
        time.sleep(random.uniform(9.5, 10.5))  # Wait for the submission to complete
        print(f"fill_additional_details_2_finished")
    except Exception as e:
        print(f"Error filling additional details2 for : {e}")
        driver.quit()  # Quit the driver immediately upon error
        raise  # Re-raise the exception for further handling

def log_error(row, log_file='error_log.txt'):
    with open(log_file, 'a+') as f:
        forename = row.get('forename', 'N/A')  # Get forename from row, default to 'N/A' if not present
        surname = row.get('surname', 'N/A')  # Get surname from row, default to 'N/A' if not present
        email = row.get('email_address', 'N/A')  # Get surname from row, default to 'N/A' if not present
        f.write(f"Error processing row: forename={forename}, surname={surname}, email = {email}\n")


def type_slowly(element, text, delay_range=(0.3, 0.5)):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))  # Random delay between each keystroke
# Main function to iterate over rows in the Excel file
def main():
    global user_password
    successful_count = 1
    location_index = 0
    # Fetch proxies from the URL
    if 'result' not in data.columns:
        data['result'] = ''
    data['result'] = data['result'].astype(object)
    if 'password' not in data.columns:
        data['password'] = ''
    data['password'] = data['password'].astype(object)

    for index, row in data.iloc[0:].iterrows():
        # if(row['result'] == 'fail'):
            # location = random.choice(locations)
        location = locations[location_index]
        with ExpressVpnApi() as api:
            ExpressVpnApi().connect(location["id"])
        time.sleep(10)
        location_index = (location_index + 1) % 4
        driver = setup_driver()  # Set up the driver for the current proxy
        result = "AR or Typo"
        
        try:
            
            fill_initial_form(driver, row)
            result = "fail"
            fill_additional_details_1(driver, row)
            fill_additional_details_2(driver, row)
            
            # maybelater = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NO, MAYBE LATER')))
            maybelater = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'NO, MAYBE LATER')]")))
            move_and_click(driver, maybelater, False)
            # maybelater.click()
            print("maybe_later_label clicked")
            result = "CNV"

            time.sleep(random.uniform(1.0, 2.0))
            depositButton = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            move_and_click(driver, depositButton, False)
            # depositButton.click()
            print("deposit_button clicked")

            time.sleep(random.uniform(1.0, 2.0))
            finalLabel = driver.find_element(By.XPATH, "//label[@for='fundprotection']")
            move_and_click(driver, finalLabel, False)
            # finalLabel.click()
            print("policy_label clicked")


            time.sleep(random.uniform(1.0, 2.0))
            finalbutton = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            move_and_click(driver, finalbutton, False)
            # finalbutton.click()
            print("policy_button clicked")

            time.sleep(random.uniform(5.0, 10.0))
            liveChat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-chat') and contains(@class, 'theme-chat')]")))
            
            print("OK")
            result = "SUCCESS"
            successful_count += 1
            

        except Exception as e:
            print(f"Error accessing the URL: {e}")
            log_error(row)  # Log the row that caused an error
        finally:
            # auth_thread.join()  # Wait for the authentication thread to finish
            data.at[index, 'result'] = result
            data.at[index, 'password'] = user_password
            driver.quit()  # Ensure the browser is closed after processing.
            time.sleep(3)
   

            if successful_count % 20 == 0:
                print("20 accounts registered successfully. Resting for 2 minutes...")
                time.sleep(120)  # Sleep for 2 minutes
            data.to_excel(file_path, index=False)
if __name__ == "__main__":
    main()
