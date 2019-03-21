from selenium import webdriver
import selenium as se
import json
import urllib.request

DOT_CAMERA_LIST_URL = "https://webcams.nyctmc.org/new-data.php?query="
data = {} 
data['Camera'] = []

options = se.webdriver.ChromeOptions()
options.add_argument('headless')

driver = se.webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)

file = json.loads(urllib.request.urlopen(DOT_CAMERA_LIST_URL).read())

for cam in file['markers']:
    driver.get("https://webcams.nyctmc.org/google_popup.php?cid="+cam['id'])
    img = driver.find_element_by_id('watermark_box').find_element_by_tag_name("img")
    if "cctv" in img.get_attribute("src"):
         data['Camera'].append({  
        'locId': cam['id'],
        'latitude': cam['latitude'],
        'longitude': cam['longitude'],
        'content': cam['content'],
        'url': img.get_attribute("src")
        
        })
        
with open('cam.json', 'w') as outfile:  
    json.dump(data, outfile)
driver.quit()
