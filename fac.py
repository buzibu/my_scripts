from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import requests
import shutil

import re

import pickle
import os
import logging
from random import randint
from time import sleep

logging.basicConfig(format='%(levelname)s: [%(asctime)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S', filename='logfile.log', level=logging.INFO)



driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)



driver.get("https://www.facebook.com/xxxxx") # url of the first image in album

# element = WebDriverWait(driver, 10).until(
#     EC.title_is("11th Pancharevo Trail Marathon 2022")
# )


# html = driver.page_source

# match = re.search(r'"id":"(\d*?)"},"media"', html).group(1)

# element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, match))
# )


# driver.find_element_by_id(match).click()

exists_counter = 0

while exists_counter<10:
    
 #   element = WebDriverWait(driver, 10).until(
 #       EC.presence_of_element_located((By.CLASS_NAME, "ji94ytn4"))
 #   )
    xpath_value = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img"

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,xpath_value))
    )
    
    #image_url =  driver.find_element_by_class_name("ji94ytn4").get_attribute("src")
    #image_url = driver.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img")
    
    image_url = driver.find_elements(by=By.XPATH, value=xpath_value)[0].get_attribute("src")
    print(image_url)

    ## Set up the image URL and filename
    filename = image_url.split("/")[-1]
    filename = filename.split("?")[0]
    
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)
    
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        

        if not os.path.isfile(f'./output/{filename}'):
            # Open a local file with wb ( write binary ) permission.
            with open(f'./output/{filename}','wb') as f:
                shutil.copyfileobj(r.raw, f)
                print('Image sucessfully Downloaded: ',filename)
                get_url = driver.current_url
                logging.info(f'Image sucessfully Downloaded: {filename} url:{get_url}')
                exists_counter = 0
        else:
            print('Image Exists')
            get_url = driver.current_url
            logging.info(f'Image Exists: {filename} url:{get_url}')
            exists_counter += 1
        
    else:
        print(f'Image Couldn\'t be retreived: {filename}')
        get_url = driver.current_url
        logging.info(f'Image Couldn\'t be retreived: {filename} url:{get_url}')
    
    sleep(randint(5,30))
    driver.find_element_by_css_selector('body').send_keys(Keys.RIGHT)


driver.close()