from importantClass import *


class RunFile:
    def __init__(self):
        self.user_password =  "Jason1234!"
        self.locations =  self.getConfig()['locations']
        self.file_path = 'data.xlsx' 
        self.data = pd.read_excel(self.file_path)
        self.mainClass = FillWebsite()
        self.driver = self.mainClass.setup_driver() 
    
    def getConfig(self):
        # set up conffig file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    
    def getUrl(self):
        # url of the proxy list
        with open('url.txt', 'r') as file:
            landing_url = file.read().strip()
        return landing_url
    
    def select_gender(self,driver, gender, row):
        print(f"select_gender_started")
        try:
            if gender.lower() == "mr":
                male_label = driver.find_element(By.XPATH, "/html/body/div[5]/div/form/div[2]/div[1]/label")
                self.mainClass.move_and_click(driver, male_label)

            elif gender.lower() == "ms":
                female_label = driver.find_element(By.XPATH, "/html/body/div[5]/div/form/div[2]/div[2]/label")
                self.move_and_click(driver, female_label)

            else:
                male_label = driver.find_element(By.XPATH, "/html/body/div[5]/div/form/div[2]/div[1]/label")
                self.move_and_click(driver, male_label)
                
            print(f"select_gender_finished")
        except Exception as e:
            print(f"Error selecting gender: {e}")
            driver.quit()  # Quit the driver immediately upon error
            raise  # Re-raise the exception for further handling
    
    def click_enter_address_manually(self,driver, row):
        try:
            if self.mainClass.is_element_present(driver,By.XPATH,'/html/body/div[5]/div/form/div[9]/span'):
                print("Element FOUND manuually.")
                # driver.implicitly_wait(15)  
                continueButton = driver.find_element(By.XPATH, '/html/body/div[5]/div/form/div[9]/span')
                time.sleep(random.uniform(0.5, 0.1))
                print("pressing once")
                self.mainClass.move_and_click(driver, continueButton)
                time.sleep(random.uniform(0.5, 0.1))
                print("pressing trice")
                # try:
                #     self.mainClass.move_and_click(driver, continueButton)
                #     # driver.implicitly_wait(15)  
                # except  Exception as e :
                #     print(f"pressing 2 error: {e}")
                
                time.sleep(random.uniform(0.5, 0.1))
                # try:
                #     self.mainClass.move_and_click(driver, continueButton)
                #     # driver.implicitly_wait(15)  
                # except  Exception as e :
                #     print(f"pressing 3 error: {e}")
            else:
                print("Element does not exist or is hidden manually.")
                
            time.sleep(random.uniform(0.5, 0.1))
            print(f"click_continue_button_finished")
        except Exception as e:
            print(f"Error clicking the continue button: {e}")
            driver.quit()  # Quit the driver immediately upon error
            raise  # Re-raise the exception for further handling

    
    def fill_additional_details_1(self,driver, row):
        print(f"fill_additional_details_1_started")
        try:
            # self.select_gender(driver, row['title'],row)
            firstname = driver.find_element(By.ID, "firstname")
            lastname = driver.find_element(By.ID, "lastname")
            self.mainClass.move_and_click(driver, firstname)
            self.mainClass.type_slowly(firstname, row['forename'])
            self.mainClass.move_and_click(driver, lastname)
            self.mainClass.type_slowly(lastname, row['surname'])

            date_of_birth = pd.to_datetime(row['date_of_birth']).strftime('%y/%m/%Y')


            dayElement = driver.find_element(By.ID, "dateOfBirth")
            self.mainClass.move_and_click(driver,dayElement)
            # all_date =  str(date_of_birth.day) + str(date_of_birth.month) + str(date_of_birth.year)
            self.mainClass.type_slowly(dayElement, date_of_birth)

            self.mainClass.move_and_click(driver,dayElement)
            
            ll = driver.find_element(By.ID, "number")
            self.mainClass.move_and_click(driver, ll)
            self.mainClass.type_slowly(ll, str(row['Telephone']).split(".")[0])
            
            
            self.click_enter_address_manually(driver, row)
            
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
            address_input = driver.find_element(By.ID, "line1")
            self.mainClass.move_and_click(driver, address_input, False)
            self.mainClass.type_slowly(address_input, address)
            
            
            city_input = driver.find_element(By.ID, "city")
            self.mainClass.move_and_click(driver, city_input, False)
            self.mainClass.type_slowly(city_input, row['ad4'])
            
            zip_input = driver.find_element(By.NAME, "postalcode")
            self.mainClass.move_and_click(driver, zip_input,False)
            self.mainClass.type_slowly(zip_input, row['postcode'])
                
            yy = driver.find_element(By.ID, "sawPin")
            self.mainClass.move_and_click(driver, yy)
            self.mainClass.type_slowly(yy, str(row['pin']).split(".")[0])
            
            ll = driver.find_element(By.ID, "select-all-checkbox")
            self.mainClass.move_and_click(driver, ll)
           
            kk = driver.find_element(By.ID, "tandc")
            self.mainClass.move_and_click(driver, kk)
            
            
            
          
            
            time.sleep(random.uniform(0.5, 1.0))
            self.click_continue_regiter(self.driver,3)
            time.sleep(30)
            # monthElement = driver.find_element(By.NAME, "month")
            # type_slowly(monthElement, str(date_of_birth.month))
            # move_and_click(driver,monthElement)
            
            # yearElement=driver.find_element(By.NAME, "year")
            # type_slowly(yearElement, str(date_of_birth.year))
            # move_and_click(driver,yearElement)

            
            # click_continue_button(driver,2)
            
            print(f"fill_additional_details_1_finished")
        except Exception as e:
            print(f"Error filling additional details1: {e}")
            driver.quit()  # Quit the driver immediately upon error
            raise  # Re-raise the exception for further handling

    
    def click_continue_regiter(self,driver,step):
        print(f"click_continue_button_started")
        try:
            if self.mainClass.is_element_present(driver,By.XPATH,'/html/body/div[5]/div/form/div[18]/button'):
                print("Element FOUND. register")
                # driver.implicitly_wait(15)  
                continueButton = driver.find_element(By.XPATH, '/html/body/div[5]/div/form/div[18]/button')
                time.sleep(random.uniform(0.5, 0.1))
                print("pressing once")
                self.mainClass.move_and_click(driver, continueButton)
                time.sleep(random.uniform(0.5, 0.1))
                print("pressing trice")
                try:
                    self.mainClass.move_and_click(driver, continueButton)
                    # driver.implicitly_wait(15)  
                except  Exception as e :
                    print(f"pressing 2 error: {e}")
                
                time.sleep(random.uniform(0.5, 0.1))
                try:
                    self.mainClass.move_and_click(driver, continueButton)
                    # driver.implicitly_wait(15)  
                except  Exception as e :
                    print(f"pressing 3 error: {e}")
            else:
                print("Element does not exist or is hidden. register")
            
            
            
            time.sleep(random.uniform(0.5, 0.1))
            print(f"click_continue_button_finished")
        except Exception as e:
            print(f"Error clicking the continue button: {e}")
            driver.quit()  # Quit the driver immediately upon error
            raise  # Re-raise the exception for further handling


    def click_continue_button(self,driver,step):
        print(f"click_continue_button_started")
        try:
            if self.mainClass.is_element_present(driver,By.XPATH,'/html/body/div[5]/div/div[2]/div/form/div[4]/button'):
                print("Element FOUND.")
                # driver.implicitly_wait(15)  
                continueButton = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div/form/div[4]/button')
                time.sleep(random.uniform(0.5, 0.1))
                print("pressing once")
                self.mainClass.move_and_click(driver, continueButton)
                time.sleep(random.uniform(0.5, 0.1))
                print("pressing trice")
                try:
                    self.mainClass.move_and_click(driver, continueButton)
                    # driver.implicitly_wait(15)  
                except  Exception as e :
                    print(f"pressing 2 error: {e}")
                
                time.sleep(random.uniform(0.5, 0.1))
                try:
                    self.mainClass.move_and_click(driver, continueButton)
                    # driver.implicitly_wait(15)  
                except  Exception as e :
                    print(f"pressing 3 error: {e}")
            else:
                print("Element does not exist or is hidden.")
            
            
            
            time.sleep(random.uniform(0.5, 0.1))
            print(f"click_continue_button_finished")
        except Exception as e:
            print(f"Error clicking the continue button: {e}")
            driver.quit()  # Quit the driver immediately upon error
            raise  # Re-raise the exception for further handling

    def fill_initial_form(self, row):
        
        print(f"fill_initial_form started")
        try:
            # Navigate to the registration page
            self.driver.maximize_window()
            self.driver.get(self.getUrl())  # Replace with the actual URL
        
            print("clicking accept cookier")
            try:
                join_button1 = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
                )
                self.mainClass.move_and_click(self.driver, join_button1)
            except:
                print("could not get cookiers")
            print("Clicking the join button")
            join_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div/a'))
            )
            time.sleep(random.uniform(2.0, 3.0))
            # Click the button
            print("clicking the button")
            join_button.click()
            # self.mainClass.move_and_click(self.driver, join_button)
            print("Join button clicked successfully")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            

            # Fill in the initial form fields
            phone_last_three = str(row['Telephone']).split(".")[0][:3]  # Get the last three digits of the telephone number
            user_id = f"{row['forename']}{row['surname']}{phone_last_three}"
            user_id = user_id.replace(" ", "")
            user_id = user_id.replace("'", "")
            user_id = user_id.lower()
            email_input = self.driver.find_element(By.ID, "email")
            username_input = self.driver.find_element(By.ID, "register_username")
            password_input = self.driver.find_element(By.ID, "register_password")
            user_password = self.mainClass.generate_strong_password(random.randint(8, 13))
            
            pyautogui.click()  # Perform the click
            time.sleep(random.uniform(1,2))
            self.mainClass.move_and_click(self.driver, email_input)
            # # email_input.click()
            time.sleep(random.uniform(0.1, 0.3))
            self.mainClass.move_and_click(self.driver, username_input)
            time.sleep(random.uniform(0.1, 0.3))
            self.mainClass.move_and_click(self.driver, password_input)
            time.sleep(random.uniform(0.1, 0.3))

            self.mainClass.move_and_click(self.driver, email_input)
            self.mainClass.type_slowly(email_input, row['email_address'].replace(" ", ""))
            # # email_input.send_keys(Keys.RETURN)
            print(f"emailaddress filled as '{row['email_address']}'")
            time.sleep(random.uniform(0.5, 1.5))

            self.mainClass.move_and_click(self.driver, username_input)
            self.mainClass.type_slowly(username_input, user_id)
            # # username_input.send_keys(Keys.RETURN)
            print(f"username filled")

            
            
            time.sleep(random.uniform(0.5, 1.5))
            self.mainClass.move_and_click(self.driver, password_input)
    
            
            self.mainClass.type_slowly(password_input, user_password)
            print(f"password filled")
            time.sleep(random.uniform(0.5, 1.5))

            
            self.mainClass.move_and_click(self.driver, username_input)
            time.sleep(random.uniform(0.5, 1.5))
            self.mainClass.move_and_click(self.driver, password_input)
            time.sleep(random.uniform(0.5, 1.5))
            # email_input.click()
            self.mainClass.move_and_click(self.driver, email_input)
            time.sleep(random.uniform(0.5, 1.5))
            self.mainClass.move_and_click(self.driver, username_input)
            continue_button_1_clickable = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[2]/div/form/div[4]/button')))
            time.sleep(random.uniform(0.5, 1.0))
            
            # user_password.submit()
            # time.sleep(random.uniform(0.5, 0.1))
            # print(f"click_continue_button_finished")
         
            self.click_continue_button(self.driver,1)
            print(f"fill_initial_form finished")
            time.sleep(2.5)
        except Exception as e:
            print(f"Error filling initial form for {row['forename']} {row['surname']}: {e}")
            self.driver.quit()  # Quit the driver immediately upon error
            raise  # Re-raise the exception for further handling

        
    def main(self):
     
        successful_count = 1
        location_index = 0
        # Fetch proxies from the URL
        if 'result' not in self.data.columns:
            self.data['result'] = ''
        self.data['result'] = self.data['result'].astype(object)
        if 'password' not in self.data.columns:
            self.data['password'] = ''
        self.data['password'] = self.data['password'].astype(object)

        for index, row in self.data.iloc[0:].iterrows():
            # if(row['result'] == 'fail'):
                # location = random.choice(locations)
            location = self.locations[location_index]
            # undo later
            # with ExpressVpnApi() as api:
            #     ExpressVpnApi().connect(location["id"])
            time.sleep(10)
            location_index = (location_index + 1) % 4
             # Set up the driver for the current proxy
            result = "AR or Typo"
          
            
            try:
                
                self.fill_initial_form(row)
                result = "fail"
                self.fill_additional_details_1(self.driver, row)
                # fill_additional_details_2(driver, row)
                
                # # maybelater = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'NO, MAYBE LATER')))
                # maybelater = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'NO, MAYBE LATER')]")))
                # move_and_click(driver, maybelater, False)
                # # maybelater.click()
                # print("maybe_later_label clicked")
                # result = "CNV"

                # time.sleep(random.uniform(1.0, 2.0))
                # depositButton = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
                # move_and_click(driver, depositButton, False)
                # # depositButton.click()
                # print("deposit_button clicked")

                # time.sleep(random.uniform(1.0, 2.0))
                # finalLabel = driver.find_element(By.XPATH, "//label[@for='fundprotection']")
                # move_and_click(driver, finalLabel, False)
                # # finalLabel.click()
                # print("policy_label clicked")


                # time.sleep(random.uniform(1.0, 2.0))
                # finalbutton = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
                # move_and_click(driver, finalbutton, False)
                # # finalbutton.click()
                # print("policy_button clicked")

                # time.sleep(random.uniform(5.0, 10.0))
                # liveChat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-chat') and contains(@class, 'theme-chat')]")))
                
                # print("OK")
                # result = "SUCCESS"
                # successful_count += 1
                

            except Exception as e:
                print(f"Error accessing the URL: {e}")
                # log_error(row)  # Log the row that caused an error
            finally:
                pass
                # auth_thread.join()  # Wait for the authentication thread to finish
                # undo later
                # data.at[index, 'result'] = result
                # data.at[index, 'password'] = user_password
                # driver.quit()  # Ensure the browser is closed after processing.
                # time.sleep(3)
    

                # if successful_count % 20 == 0:
                #     print("20 accounts registered successfully. Resting for 2 minutes...")
                #     time.sleep(120)  # Sleep for 2 minutes
                # data.to_excel(file_path, index=False)


app = RunFile()
app.main()