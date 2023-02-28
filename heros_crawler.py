# code to crawl all of hero icons (79 hero icons) from the provided website
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from PIL import Image

# setting options for chrome driver to use headless mode
# Options.headless = False
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver_path = '//Users/quan.ha/Downloads/chromedriver_mac64/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path,options=options)

#get the entire page source through web url
driver.get('https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki')

#find element contain all list of images
h1 = driver.find_element(By.ID,'champion-grid')
image_list = h1.find_element(By.TAG_NAME,'ol')
image_list = h1.find_elements(By.TAG_NAME,'li')

count = 0
#loop over images from the list to get details of each
for i in range(len(image_list)):
    #get image url from its attribute
    image_path = image_list[i].find_element(By.TAG_NAME,'img').get_attribute('data-src')
    print(image_path)

    #get hero name from a tag
    hero_name = image_list[i].find_element(By.TAG_NAME, 'img').get_attribute('alt')
    # hero_name = image_list[i].find_elements(By.TAG_NAME,'a')[1].text

    # #save image under its hero name to the folder 'hero_icons'
    img = Image.open(requests.get(image_path, stream=True).raw)
    img = img.convert('RGB')
    img.save('./hero_icons/'+hero_name+'.jpg')
    count += 1
