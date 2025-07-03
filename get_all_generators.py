from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from master_dict_file import master_keys
from master_dict_file import master_dict

options = ChromeOptions()

# I cannot figure out how to make headless mode work, so I'm settling for the rather ghetto method of rendering the window very far offscreen to mimic it
# options.add_argument("--headless=new")
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--start-maximized")
options.add_argument("--window-position=-10000,0")

# generatorlinks = []

# # This function gets the link to all the different name generators
# # I only needed to use it once for fantasy and once for real world names, but you could run it every time to check for new ones
# def find_all_generators(url, selector):
#
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)
#
#     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
#     text_box = driver.find_elements(By.CSS_SELECTOR, selector)
#     for i in text_box:
#         generatorlinks.append(i.get_attribute("href"))
#
# # x is the website, y is the container for all "fantasy/folklore" names, and z is the container for all "real world" names
# # x = "https://www.fantasynamegenerators.com/"
# # y = "#navmenus > ul > li:nth-child(2) .mainOl a"
# # z = "#splitNav a"
#
# find_all_generators(x, y)
# find_all_generators(x, z)
#
# This saves all the entries into a nicely formatted list in a new file
# I simply copied and pasted it from there so that this none of this had to be run again
# with open("output.py", "w") as f:
#     f.write("my_list = ")
#     json.dump(generatorlinks, f, indent=2)


# test_dict = {
#   "Alien Names": "https://www.fantasynamegenerators.com/alien-names.php",
#   "Amazon Names": "https://www.fantasynamegenerators.com/amazon-names.php",
#   "Anansi Names": "https://www.fantasynamegenerators.com/anansi-names.php",
#   "Angel Names": "https://www.fantasynamegenerators.com/angel-names.php",
#   "Animal Species Names": "https://www.fantasynamegenerators.com/animal-species-names.php",
#   "Animatronic Names": "https://www.fantasynamegenerators.com/animatronic-names.php",
#   "Anime Character Names": "https://www.fantasynamegenerators.com/anime-character-names.php",
#   "Anthousai Names": "https://www.fantasynamegenerators.com/anthousai-names.php",
#   "Anz\u00fb Names": "https://www.fantasynamegenerators.com/anzu-names.php",
#   "Apocalypse/Mutant Names": "https://www.fantasynamegenerators.com/apocalypse-mutant-names.php",
#   "Artificial Intelligence Names": "https://www.fantasynamegenerators.com/artificial-intelligence-names.php",
#   "Bandit Names": "https://www.fantasynamegenerators.com/bandit-names.php",
#   "Banshee Names": "https://www.fantasynamegenerators.com/banshee-names.php",
#   "Barbarian Names": "https://www.fantasynamegenerators.com/barbarian-names.php",
#   "Basilisk Names": "https://www.fantasynamegenerators.com/basilisk-names.php",
#   "Birdfolk Names": "https://www.fantasynamegenerators.com/birdfolk-names.php",
#   "Bluecap Names": "https://www.fantasynamegenerators.com/bluecap-names.php",
#   "Bounty Hunter Names": "https://www.fantasynamegenerators.com/bounty-hunter-names.php"
# }


# This function retrieves the raw text of a JS file. It's really intended
# to be called in the function beneath it several times over

def get_javascript_file(url, index):

        # Selenium driver launch
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # "head" is where the urls to the scripts are stored
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "head > title")))

        # I suspect the scripts I want are almost always exactly the 6th child of head, but just in case
        # some pages have unusual formatting, I take some extra steps to find the right element
        head = driver.find_elements(By.XPATH, "/html/head/script[following-sibling::title]")

        # This section takes the url of the main name generator and looks through its html for
        # the link to the actual generation JS script. You can't just derive it from the main url;
        # sometimes the script's url is named logically, but sometimes it has arbitrary characters
        # at the end of it. Additionally, sometimes it's in the form xyNames.js, while other times
        # it will be, xy.js, xNames.js, etc. So instead it looks for all .js and ignores the four
        # other scripts universally found in these urls.
        script_url = str()
        for i in head:
            # Ignore script tags that have the 'async' attribute
            if i.get_attribute("async") is not None:
                continue
            src = str(i.get_attribute("src"))
            if ".js" in src and all(x not in src for x in ["saving", "banner", "randomGen", "google", "swear"]):
            # if ".js" in src and "saving" not in src and "banner" not in src and "randomGen" not in src and "ajax" not in src:
                script_url = src
                break
        if not script_url:
            print("Couldn't find script in head")
            quit()

        # Now that we have the script's personal url, we can extract the text from it

        # Selenium has to close and open the browser first, otherwise there will be a
        # Cloudflare error
        driver.quit()
        driver = webdriver.Chrome(options=options)
        driver.get(script_url)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        script = (driver.find_element(By.CSS_SELECTOR, "body")).text

        # Now we save the raw script text in a special file, in which every single
        # script will be stored in a dictionary, with the regular generator name
        # as a key and the function text as a string value
        # Some scripts, like "Anansi Names," have special characters in them, and
        # encoding="utf-8" prevents them from throwing an error and writes them successfully
        # with open("all_js_scripts.py", "a", encoding="utf-16") as f:
        #     f.write(f"'{master_keys[index]}':\n\n'''{script}''',\n\n")
        print(script.encode("utf-8").decode("latin1"))
        driver.quit()


# Runs the above function for a dictionary. If it does several entries without
# error but then something goes wrong, starting_index makes it easy to pick
# up where it left off without starting over

def get_many_javascript_files(dictionary, starting_index=0):
    for index, i in enumerate(dictionary, start=starting_index):
        url = dictionary[master_keys[index]]
        get_javascript_file(url, index)


# get_many_javascript_files(master_dict, 18)


get_javascript_file("https://www.fantasynamegenerators.com/anansi-names.php", 2)