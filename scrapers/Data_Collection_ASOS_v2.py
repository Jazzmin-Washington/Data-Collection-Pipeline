#%%
# ASOS Website
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import urllib3 
from bs4 import BeautifulSoup

import time

class Scraper():
    def __init__(self):
        self.driver = Chrome('./chromedriver')
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&nlid=ww|sale|shop+sale+by+product|sale+view+all'
        self.driver.get(url)
        self.shop_list =[]
        self.shop_data = []
        self.shop_link_list = []
        self.imagesrc_list = []
        self.full_product_data = []
        self.full_item_list = {'product_id': [],'product_name': [], 'image':[], 'previous_price':[], 'sale_price': [], 'color':[], 'product_details':[], 'sizes': []}
        self.load_pages = 0
        self.delay = 10
    
    def load_and_accept_cookies(self):
        time.sleep(10)
        accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
        accept_cookies_button.click()
        time.sleep(1)

    

    def get_product_links(self):
        time.sleep(5)
        self.clothing_container = self.driver.find_element_by_xpath('//div[@class="_3pQmLlY"]')
        self.clothing_section = self.clothing_container.find_elements_by_xpath('./section')
        for section in self.clothing_section:
            article = section.find_elements_by_xpath('./article')
            for articles in article:
                a_tag = articles.find_element_by_tag_name('a')
                link = a_tag.get_attribute('href')
                self.shop_link_list.append(link)
                img = articles.find_element_by_tag_name('img')
                img_src = img.get_attribute('src')
                self.imagesrc_list.append(img_src)
     
        print(self.imagesrc_list)
        print(f'There are {len(self.shop_link_list)} in this link list and {len(self.imagesrc_list)} in image source list')
    
    
    def load_more_products(self):
        for i in range(5):
            time.sleep(10)
            self.load_more_button = self.driver.find_element_by_xpath('//a[@data-auto-id = "loadMoreProducts"]')
            self.actions = ActionChains(self.driver)
            self.actions.move_to_element(self.load_more_button)
            time.sleep(10)
            if self.load_pages == 0:
                self.actions.move_to_element(self.load_more_button)
                self.load_more_button.click()
                time.sleep(10)
                self.load_pages +=1
            elif self.load_pages == 5:
                self.get_product_links()
            else:
                time.sleep(10)
                self.actions.move_to_element(self.load_more_button)
                self.load_more_button.click()
                self.load_pages +=1
                

    def get_product_data(self):
        self.num_clothing_items = len(self.shop_link_list)
        for i in range(self.num_clothing_items):
            self.full_item_list['image'].append(self.imagesrc_list[i])
            time.sleep(10)
            self.driver.get(self.shop_link_list[i])
            '''
            Need to add popup button
            '''

            try:
               time.sleep(10)
                self.show_more_button = self.driver.find_element_by_xpath('//a[@class="show"]') 
                self.actions.move_to_element(self.show_more_button)
                self.show_more_button.click()
            except NoSuchElementException:
                pass
            try:
                self.product_id = self.driver.find_element_by_xpath('//div[@class="product-code"]').text
                self.clean_product_id = self.product_id.replace("PRODUCT CODE", "Product Code:")
                self.product_id_num = self.clean_product_id.replace("Product Code:", "")
                self.full_item_list['product_id'].append(self.clean_product_id)
          
            except NoSuchElementException:
                self.full_item_list['product_id'].append('None')

            
            try:
                product_header = self.driver.find_element_by_xpath('//div[@class="product-hero"]')
                product_name = product_header.find_element_by_xpath('./h1').text
                self.full_item_list['product_name'].append(product_name)
            except NoSuchElementException:
                self.full_item_list['product_name'].append('None')

            try:
                previous_price = self.driver.find_element_by_xpath('//span[@data-id ="rrp-price"]').text
                self.full_item_list['previous_price'].append(previous_price)
            except NoSuchElementException:
                self.full_item_list['previous_price'].append('None')

            try:
                sale_price = self.driver.find_element_by_xpath('//span[@data-id="current-price"]').text
                self.full_item_list['sale_price'].append(sale_price)
            except NoSuchElementException:
                self.full_item_list['sale_price'].append('None')

            try:
                colour = self.driver.find_element_by_xpath('//span[@class="product-colour"]').text
                self.full_item_list['color'].append(colour)
            except NoSuchElementException:
                 self.full_item_list['color'].append('None')

            try:
                description = self.driver.find_element_by_xpath('//div[@class = "product-description"]').text
                ab_description = description.replace("PRODUCT DETAILS", "")

                self.full_item_list['product_details'].append(ab_description)
            except NoSuchElementException:
                self.full_item_list['product_details'].append('None')


            try:
                sizes = self.driver.find_element_by_xpath('//select[@data-id="sizeSelect"]').text
                sizes = sizes.replace("Please select", "")
                self.full_item_list['sizes'].append(sizes)
            except NoSuchElementException:
                self.full_item_list['sizes'].append('None')


            self.organized_data  = {self.product_id_num:{'name':[product_name], 'previous_price':[previous_price], 'sale price':[sale_price], 'color':[colour], 'description':[ab_description], 'sizes':[sizes]}}
            self.full_product_data.append(self.organized_data)
            print(self.organized_data)
            

    def scrape_website(self):
        self.load_and_accept_cookies()
        self.get_product_links()
        self.driver.close()
    
new_Scraper_ASOS= Scraper()
new_Scraper_ASOS.scrape_website() 

            
# %%
