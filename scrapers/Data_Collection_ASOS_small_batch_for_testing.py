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
import urllib.request
from tqdm import tqdm
import pandas as pd
import json
import uuid
import os
from os.path import exists
import time

# To import class later
url = 'https://www.asos.com/women'
url_1 = 'https://www.asos.com/women/ctas/generic-promos/promotion-6/cat/?cid=28249&ctaref=hp|ww|prime|hero|1|edit|jublieeupto70off'
url_2 = 'https://www.asos.com/women/sale/cat/?cid=7046&nlid=ww|sale|shop+sale+by+product|sale+view+all'


class Scraper():
    #Variables that were initialised including necessary lists, drivers and dictionaries 
    def __init__(self):
        self.driver = Chrome('./chromedriver')        
        self.driver.get(url)
        self.shop_link_list = []
        self.imagesrc_list = []
        self.full_product_data = []
        self.full_product_id = []
        self.full_item_list = {'product_id': [],'product_name': [], 'image':[], 'previous_price':[], 'sale_price': [], 'sale_percentage':[], 'color':[], 'product_details':[], 'sizes': []}
        self.load_pages = 0
        self.n_pages = 5
        self.actions = ActionChains(self.driver)
        self.delay = 10
    
    def nav_to_sale_pg(self):
        self.driver.maximize_window()
        time.sleep(5)
        sales_button = self.driver.find_element_by_xpath('//button[@data-id="57242f2c-d207-471c-95b1-31d6839df360"]')
        view_all_button = self.driver.find_element_by_xpath('//a[@class="_1cjL45H _2Y7IAa_ CLdGn9X _1XjY6Zd _1zz7j1l"]')
        self.driver.implicitly_wait(10)
        self.actions.move_to_element(sales_button).click_and_hold().perform()
        self.driver.implicitly_wait(10)
        view_all_button.click()
        self.driver.implicitly_wait(10)
         
        if self.driver.current_url != url_1  and self.driver.current_url != url_2 :
            self.actions.move_to_element(sales_button).click_and_hold().perform()
            time.sleep(1)
            view_all_button.click()
            self.driver.implicitly_wait(10)
 
    # Clicks the accept cookies button on the selenium driver
    def load_and_accept_cookies(self):
        self.driver.implicitly_wait(10)
        accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
        self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True' );});",accept_cookies_button)
        accept_cookies_button.click()
        time.sleep(2)
        self.unit_Test_Cookies = accept_cookies_button.get_attribute("automationTrack")
        return self.unit_Test_Cookies
   

    # Collects the links on all the loaded products and saved to list
    def get_product_links(self):
        time.sleep(2)
        self.clothing_container = self.driver.find_element_by_xpath('//div[@class="_3pQmLlY"]')
        self.clothing_section = self.clothing_container.find_elements_by_xpath('./section')
        for section in self.clothing_section:
            article = section.find_elements_by_xpath('./article')
            time.sleep(2)
            for articles in article:
                a_tag = articles.find_element_by_tag_name('a')
                self.link = a_tag.get_attribute('href')
                self.shop_link_list.append(self.link)
        
        # Confirms the necessary links have been collected       
        print(f'There are {len(self.shop_link_list)} in this link list')
        return self.shop_link_list

    # Selects the 'load more' button of the sale website to load more products
    def load_more_products(self):
        # n_pages was used to allow user to select later the number of pages they want to load
      
        while self.load_pages != self.n_pages:
            self.driver.implicitly_wait(10)
            self.load_more_button = self.driver.find_element_by_xpath('//a[@data-auto-id = "loadMoreProducts"]')
            self.actions.move_to_element(self.load_more_button)
            self.load_more_button.click()
            self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True');});",self.load_more_button)
            self.unit_Test_Load_1 = self.load_more_button.get_attribute("automationTrack")
            self.driver.implicitly_wait(10)
            self.load_pages +=1

        if self.load_pages == self.n_pages:
            self.unit_loaded_pages = True
                 
        return  self.unit_loaded_pages, self.unit_Test_Load_1, self.n_pages, self.load_pages



    # Collects the data from the each of the collected links(product code, sale price etc.)
    def get_product_data(self):
        self.num_clothing_items = len(self.shop_link_list)
        for i in tqdm(range(10), 'Collecting Data from Links'):
            self.driver.implicitly_wait(10)
            self.driver.get(self.shop_link_list[i])
            time.sleep(1)

            # Selects the 'X" on the 'student discount' popup
            try:
                self.driver.implicitly_wait(10)
                self.popup = self.driver.find_element_by_xpath('//*[@id="att_lightbox_close"]')
                self.popup.click()
            except (ElementNotInteractableException, NoSuchElementException):
                pass
            
            # Selects the show more button to expose the relevant data for scraping  
            try:
                self.driver.implicitly_wait(10)
                self.show_more_button = self.driver.find_element_by_xpath('//a[@class="show"]') 
                self.driver.implicitly_wait(10)
                self.actions.move_to_element(self.show_more_button)
                self.show_more_button.click()
            except NoSuchElementException:
                pass
            
            # Collects the product id for each of the products
            try:
                self.product_id = self.driver.find_element_by_xpath('//div[@class="product-code"]')
                self.product_id_num =self.product_id.find_element_by_xpath('./p').text
                self.full_item_list['product_id'].append(self.product_id_num)
                self.full_product_id.append(self.product_id_num)
            except NoSuchElementException:
                self.product_id_num = (str(uuid.uuid4())[:9].replace("-",""))
                self.full_item_list['product_id'].append(self.product_id_num)
                self.full_product_id.append(self.product_id_num)
           

            # Collects the image source for each of the product to download in get_images() function
            try:
                img = self.driver.find_element_by_xpath('//div[@class="image-container zoomable"]')
                image = img.find_element_by_xpath('./img')
                self.image_src = image.get_attribute('src')
                self.full_item_list['image'].append(self.image_src)
                self.imagesrc_list.append(self.image_src)
                

            except NoSuchElementException:
                self.full_item_list['image'].append('None')

            #Collects the product name of each of the items
            try:
                product_header = self.driver.find_element_by_xpath('//div[@class="product-hero"]')
                self.product_name = product_header.find_element_by_xpath('./h1').text.strip()
                self.full_item_list['product_name'].append(self.product_name)
            except NoSuchElementException:
                self.full_item_list['product_name'].append('None')
            
            #Collects the market price for each of the products
            try:
                self.previous_price = self.driver.find_element_by_xpath('//span[@data-id ="rrp-price"]').text
                self.previous_price = self.previous_price.replace('RRP', '')
                
                #Some of the website use the RRP tag and other used a previous_price tag
                if self.previous_price == '':
                    self.previous_price = self.driver.find_element_by_xpath('//span[@data-id ="previous-price"]').text
                    self.previous_price = self.previous_price.replace('Was', '')

                self.full_item_list['previous_price'].append(self.previous_price)
            except NoSuchElementException:
                self.full_item_list['previous_price'].append('None')

            # Collects the sale price of each of the products
            try:
                self.sale_price = self.driver.find_element_by_xpath('//span[@data-id="current-price"]').text.strip()
                self.sale_price_clean = self.sale_price.replace("Now", '')
                self.full_item_list['sale_price'].append(self.sale_price_clean)
                if self.sale_price == '':
                    self.full_item_list['sale_price'].append('Item is not on sale')
            except NoSuchElementException:
                self.full_item_list['sale_price'].append('None')
            
            # Collects the percentage difference between market and sale price of products
            try:
                self.sale_percentage = self.driver.find_element_by_xpath('//span[@class="product-discount-percent"]').text.strip()
                self.full_item_list['sale_percentage'].append(self.sale_percentage)
                if self.sale_percentage == '':
                    self.full_item_list['sale_percentage'].append('Item not on sale')
            except NoSuchElementException:
                self.full_item_list['sale_percentage'].append('None')

            # Collects the color of the items. Some have multiple colors
            try:
                self.colour= self.driver.find_element_by_xpath('//span[@class="product-colour"]').text.strip()
                
                # If there are multiple colors instead of sizes then they are accounted for below
                if self.colour == '':
                    self.colour = self.driver.find_element_by_xpath('//div[@data-test-id="colour-size-select"]').text.strip()
                    self.colour= self.colour.replace("Please select from", "")
                    self.colour = self.colour.replace("colors", 'colors:')
                self.full_item_list['color'].append(self.colour)
            except NoSuchElementException:
                self.full_item_list['color'].append('None')

            # Collects product description for each of the product
            try:
                self.description = self.driver.find_element_by_xpath('//div[@class = "product-description"]').text.replace("PRODUCT DETAILS\n", "")
                self.full_item_list['product_details'].append(self.description)
            except NoSuchElementException:
                self.description = "None"
                self.full_item_list['product_details'].append('None')
            
            # Collects the sizes for each of the products
            try:
                self.sizes = self.driver.find_element_by_xpath('//select[@data-id="sizeSelect"]').text.strip()
                self.sizes = self.sizes.replace("Please select", "")
                if self.sizes == '':
                    self.sizes = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[2]/div/div/div/div[3]/div[1]/p').text.strip()
                elif self.sizes == '':
                    self.sizes = self.driver.find_element_by_xpath('//span[@class="product-size"]')

                self.full_item_list['sizes'].append(self.sizes)
            except NoSuchElementException:
                self.full_item_list['sizes'].append('None')
    
            # Added to organize each item by their respective product id
            
            self.organized_data  = {self.product_id_num:{'name':self.product_name, 'image':self.image_src, 'previous_price':self.previous_price, 'sale price':self.sale_price_clean,'sale_percentage':self.sale_percentage, 'color':self.colour, 'description':self.description, 'sizes':self.sizes}}
            self.full_product_data.append(self.organized_data)
        return self.full_item_list, self.full_product_data, self.full_product_id
    

    # Saves the data to either a json file or a pd Dataframe/csv for later    
    def save_data(self):
        if not os.path.exists('ASOS_data'):
                os.makedirs('ASOS_data')

        with open('ASOS_data/ASOS_Women_data.json', 'w+') as fp:
            json.dump(self.full_item_list, fp,  indent=4)

        with open('ASOS_data/ASOS_Women_Org_data.json', 'w+') as fp:
            json.dump(self.full_product_data, fp,  indent=4)

        print(os.getcwd())   
        
        df1 = pd.DataFrame.from_dict(self.full_item_list) 
        df1.to_csv (r'ASOS_data/ASOS_Women_Data.csv',  header=True)
       

        if os.path.exists('ASOS_data/ASOS_Women_Data.csv') and os.path.exists('ASOS_data/ASOS_Women_Org_data.json'):
            self.saving_data = True

        return self.saving_data, 


     
    # Will download each of the images from their respective image sources for later
    def get_images(self):
        if not os.path.exists('ASOS_data/images'):
                os.makedirs('ASOS_data/images')

        self.test_images = []
        len_images = len(self.imagesrc_list)
        for i in tqdm(range(len_images), 'Downloading images'):
            id = self.full_item_list['product_id'][i] 
            image = self.imagesrc_list[i]
            urllib.request.urlretrieve(image, f"ASOS_data/images/ASOS_image_{id}.jpg")
            if os.path.exists(f"ASOS_data/images/ASOS_image_{id}.jpg"):
                self.test_images.append(True)
            else:
                self.test_images.append(False)
        return self.test_images
    

    # Final Function that calls all the functions above in the necessary order    
    def scrape_website(self):
        self.load_and_accept_cookies()
        self.nav_to_sale_pg()
        self.get_product_links()
        self.get_product_data()
        self.save_data()
        self.get_images()
        self.driver.close()
        self.driver.quit()
        
ASOS = Scraper()


# Begins the scraping process 
if __name__ == "__main__": 
    ASOS = Scraper() 
    
# %%
