import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests, os, urllib.request

print("Enter username and password for loggin in to Instagram")
username = input("Enter username: ")
password = input("Enter password: ")
account = input("Now enter the name of account to download files from: ")

options = webdriver.ChromeOptions()
# options.add_argument('headless')
path = <ENTER PATH TO chromedriver.exe>
driver = webdriver.Chrome(executable_path=path, options=options)

driver.get('https://www.instagram.com/')
time.sleep(10) # Let the user actually see something!
driver.find_element_by_xpath('//input[@name=\'username\']').send_keys(username)
driver.find_element_by_xpath('//input[@name=\'password\']').send_keys(password)
driver.find_element_by_xpath('//button[@type="submit"]').click()
time.sleep(5)

last_height = driver.execute_script("return document.body.scrollHeight")
driver.get('https://www.instagram.com/' + account)
time.sleep(5)

lst_links = []
while True:

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    match = soup.find_all('div', class_='eLAPa')
    for link in match:
        lst_links.append(link.previous_element.get('href'))
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(3)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

path = os.getcwd()
pics = os.path.join(path, 'Pics')
try:
    os.mkdir(pics)
except:
    pass

print(set(lst_links))

for link in set(lst_links):
    print(link)
    post_path = 'https://www.instagram.com' + link
    driver.get(post_path)
    print(post_path)
    time.sleep(3)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    match = soup.find('img', class_='FFVAD')['src']
    file_name = match.split('?')[0].split('/')[-1]
    file_path = os.path.join(pics, file_name)
    urllib.request.urlretrieve(match, file_path)

    if soup.find('div', class_='coreSpriteRightChevron'):
        print('MULTIPLE PICS STARTED')
        lst_post_links = []
        while soup.find('div', class_='coreSpriteRightChevron'):
            time.sleep(2)
            driver.find_element_by_class_name('coreSpriteRightChevron').click()
            time.sleep(2)
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'lxml')
            match = soup.find_all('img', class_='FFVAD')
            for link in match:
                lst_post_links.append(link['src'])
        print(set(lst_post_links))
        for link in set(lst_post_links):
            print(link)
            file_name = link.split('?')[0].split('/')[-1]
            file_path = os.path.join(pics, file_name)
            urllib.request.urlretrieve(link, file_path)
        print('MULTIPLE PICS ENDED')

driver.quit()
