"""
This is a web scraper for Honestmarys Restaurants 
"""

# Importing required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime

current_date  = datetime.now().date()

# Setting options for Chrome Webdriver
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("−−lang=en-US")
driver = webdriver.Chrome(chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 30) # Sets a wait time for driver before throwing an exception

while True:
    try:
        driver.get("https://www.honestmarys.com/locations/")
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="mapboxgl-ctrl-geocoder--input"]')))
        address_input =  driver.find_element(By.XPATH, '//input[@class="mapboxgl-ctrl-geocoder--input"]')
        address_input.click()
        address_input.send_keys("Austin")
        wait.until(EC.presence_of_element_located((By.XPATH, '//li[1]/a/div/div[@class="mapboxgl-ctrl-geocoder--suggestion-address"][1]')))
        first_suggestion = driver.find_element(By.XPATH, '//li[1]/a/div/div[@class="mapboxgl-ctrl-geocoder--suggestion-address"][1]')
        first_suggestion.click()
        break
    except Exception as e:
        print(e)
        continue

while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "locationListItem-customButton")]')))
        nav_button = driver.find_elements(By.XPATH, '//a[contains(@class, "locationListItem-customButton")]')
        menu_url = nav_button[0].get_attribute('href')
        driver.get(menu_url)
        break
    except Exception as e:
        continue

output_array = [['item_id','company_name','item_name','protein_option','price','description','added_date', 'last_modified_date', 'discontinued_date']]

while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[2]/div/div/div[2]/div/div/div/div/section/div[1]/h3')))
        sections_list = driver.find_elements(By.XPATH, "//div[@class='menuSections']/div[@class='menuSectionWrapper'][2]/div/div/div[@class='menuGroup']")
        for section in sections_list:
            category_name = section.find_element(By.XPATH, './/section/div[1]/h3').text
            sub_category_list = section.find_elements(By.XPATH, './/section/div[2]/a')
            for sub_category in sub_category_list:
                sub_category_name = sub_category.find_element(By.XPATH, './/div/div[1]/h3').text
                try:
                    price = sub_category.find_element(By.XPATH, './/div/div[2]/span').text
                except:
                    price = ''
                try:
                    des = sub_category.find_element(By.XPATH, './/div/div[3]/p').text
                except:
                    des = ''
                item = len(output_array)
                output_array.append([item, 'Honestmarys',category_name, sub_category_name, price, des, current_date, current_date, 'none'])
        break
    except Exception as e:
        print(e)
        continue

# Open the file with permissions to write, and specify formatting details
with open('honestmarys.csv', 'w', newline='', encoding='utf-8') as file:

    # Create a writing object
    writer = csv.writer(file)

    # Write output data to the CSV file
    writer.writerows(output_array)