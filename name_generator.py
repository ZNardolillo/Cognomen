# This script uses Selenium to open a chrome instance on Fantasynamegenerators.com. It's pretty much
# deprecated, but this is how I was originally going to make this project work.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from master_dict_file import master_dict

options = ChromeOptions()

# I cannot figure out how to make headless mode work, so I'm settling for the rather silly method of rendering the window very far offscreen to mimic it
# options.add_argument("--headless=new")
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--start-maximized")
options.add_argument("--window-position=-10000,0")

def generate_names(url):

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nameGen input[type="button"]')))
    genders = driver.find_elements(By.CSS_SELECTOR, '#nameGen input[type="button"]')
    result = {}

    for i in genders:

        i.click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'result')))
        text_box = driver.find_element(by=By.ID, value="result")
        value = str(i.get_attribute("value")).lower()

        if "female" in value or "feminine" in value:
            result["Female Names"] = text_box.text.split("\n")
        elif "male" in value or "masculine" in value:
            result["Male Names"] = text_box.text.split("\n")
        else:
            result["Neutral Names"] = text_box.text.split("\n")

        # print (result)
    return(result)

# print(generate_names(master_dict["Anz\u00fb Names"]))

