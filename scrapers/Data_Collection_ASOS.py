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
        self.li_tag_list = []
        self.a_tag_list = []
        self.size_options = []
        self.imagesrc_list = []
        self.full_product_data = []
        self.product_id = ''
        self.full_item_list = {'product_id': [],'product_name': [], 'image':[], 'previous_price':[], 'sale_price': [], 'color':[], 'product_details':[], 'sizes': []}
        self.load_pages = 0
        self.delay = 10
    
    def load_and_accept_cookies(self):
        time.sleep(10)
        accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
        accept_cookies_button.click()
        time.sleep(1)

    

    def get_product_links(self):
        time.sleep(10)
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
     

        print(f'There are {len(self.shop_link_list)} in this link list and {len(self.imagesrc_list)} in image source list')
    
    
    def load_more_products(self):
        for i in range(5):
            time.sleep(5)
            self.load_more_button = self.driver.find_element_by_xpath('//a[@data-auto-id = "loadMoreProducts"]')
            self.actions = ActionChains(self.driver)
            self.actions.move_to_element(self.load_more_button)
            time.sleep(5)
            if self.load_pages == 0:
                self.actions.move_to_element(self.load_more_button)
                self.load_more_button.click()
                time.sleep(5)
                self.load_pages +=1
            elif self.load_pages == 5:
                self.get_product_links()
            else:
                time.sleep(5)
                self.actions.move_to_element(self.load_more_button)
                self.load_more_button.click()
                self.load_pages +=1
                

    def get_product_data(self):
        self.num_clothing_items = len(self.shop_link_list)
        for i in range(self.num_clothing_items):
            self.full_item_list['image'].append(self.imagesrc_list[i])
            self.driver.get(self.shop_link_list[i])
            time.sleep(10)
            try:
                self.show_more_button = self.driver.find_element_by_xpath('//a[@class="show"]') 
                self.actions.move_to_element(self.show_more_button)
                self.show_more_button.click()
                time.sleep(10)
            except NoSuchElementException:
                pass
            try:
                self.product_container = self.driver.find_element_by_xpath('//div[@class="product-code"]').text
                print(self.product_container)
            except NoSuchElementException:
                self.full_item_list['product_id'].append('None')

            
            try:
                product_name = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/nav/ol/li[4]/span').text
                self.full_item_list['product_name'].append(product_name)
                print(self.full_item_list)
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
                self.full_item_list['product_details'].append(description)
            except NoSuchElementException:
                self.full_item_list['product_details'].append('None')


            try:
                drop_down_box = self.driver.find_element_by_xpath('//select[@data-id="sizeSelect"]')
                self.size_options = drop_down_box.find_elements_by_xpath('./option')
                for size in self.size_options:
                    self.full_item_list['sizes'].append(size)
                self.full_item_list['sizes'].remove[0]
            except NoSuchElementException:
                self.full_item_list['sizes'].append('None')


            self.organized_data = {self.product_container:{'product_name': [product_name], 'image':[self.imagesrc_list[i]], 'previous_price':[previous_price], 'sale_price': [sale_price], 'color':[colour], 'product_details':[description], 'sizes': [sizes]}}
            self.full_product_data.append(self.organized_data)
            print(self.full_product_data)

    def scrape_website(self):
        self.load_and_accept_cookies()
        self.load_more_products()
        self.get_product_links()
        self.get_product_data()
    
new_Scraper_ASOS= Scraper()
new_Scraper_ASOS.scrape_website()    
            
# %%
