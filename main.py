from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import os


def fill_form(price, link, address):
    for p, l, a in zip(price, link, address):
        property_location = driver.find_element(By.XPATH,
                                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]'
                                                      '/div/div[1]/div/div[1]/input')
        property_price = driver.find_element(By.XPATH,
                                             value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div'
                                                   '/div[1]/div/div[1]/input')
        property_link = driver.find_element(By.XPATH,
                                            value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/'
                                                  'div[1]/div/div[1]/input')

        property_location.send_keys(a)
        property_price.send_keys(p)
        property_link.send_keys(l)

        submit_button = driver.find_element(By.XPATH,
                                            value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
        submit_button.click()
        time.sleep(2)

        another_response = driver.find_element(By.LINK_TEXT, value="Submit another response")
        another_response.click()


# webdriver helps us automate tasks in the browser
# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# The chrome_options is sending the required headers that a website would want
driver = webdriver.Chrome(options=chrome_options)

# Some websites ask for certain header information
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Google Form we will use Selenium to fill out
GOOGLE_FORM_LINK = os.getenv('GOOGLE_FORM')
# URL of 'Zillow' clone
URL = "https://appbrewery.github.io/Zillow-Clone/"

# Get the website and get all of the html
response = requests.get(URL, headers=header)
zillow_page = response.text

# Scrape the html
soup = BeautifulSoup(zillow_page, "html.parser")

# Grab the info we want from the site
addresses_html = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor", href=True)
prices_html = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")

# Use list comprehension to get the text that we want
prices = [price.get_text()[:6].replace("+", "") for price in prices_html]
links = [link['href'] for link in addresses_html]
addresses = [address.get_text().strip().replace("|", "") for address in addresses_html]

# Get the website we want to scrape
driver.get(GOOGLE_FORM_LINK)

# function call to fill-out the form

fill_form(prices, links, addresses)


driver.quit()
