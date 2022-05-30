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
from urllib.error import ContentTooShortError
from tqdm import tqdm
import pandas as pd
import json
import os
from bs4 import BeautifulSoup
import time

# To import class later
if __name__ == "__main__":
    url = 'https://www.asos.com/women/sale/cat/?cid=7046&nlid=ww|sale|shop+sale+by+product|sale+view+all'


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
     # Clicks the accept cookies button on the selenium driver
        def load_and_accept_cookies(self):
            self.driver.implicitly_wait(10)
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
            self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True');});",accept_cookies_button)
            accept_cookies_button.click()
            time.sleep(2)
            return print(accept_cookies_button.get_attribute("automationTrack"))

        # Collects the links on all the loaded products and saved to list
        def get_product_links(self):
            time.sleep(5)
            self.clothing_container = self.driver.find_element_by_xpath('//div[@class="_3pQmLlY"]')
            self.clothing_section = self.clothing_container.find_elements_by_xpath('./section')
            for section in self.clothing_section:
                article = section.find_elements_by_xpath('./article')
                time.sleep(5)
                for articles in article:
                    a_tag = articles.find_element_by_tag_name('a')
                    link = a_tag.get_attribute('href')
                    self.shop_link_list.append(link)

            # Confirms the necessary links have been collected       
            print(f'There are {len(self.shop_link_list)} in this link list')
            return self.shop_link_list

        # Selects the 'load more' button of the sale website to load more products
        def load_more_products(self):
            for i in range(6):
                self.driver.implicitly_wait(10)
                self.load_more_button = self.driver.find_element_by_xpath('//a[@data-auto-id = "loadMoreProducts"]')
                self.actions.move_to_element(self.load_more_button)
                self.driver.implicitly_wait(10)
                if self.load_pages == 0:
                    self.actions.move_to_element(self.load_more_button)
                    self.load_more_button.click()
                    self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True');});",self.load_more_button)
                    self.driver.implicitly_wait(10)
                    self.load_pages +=1

            # n_pages were used to allow user to select later the number of pages they want to load
                elif self.load_pages == self.n_pages:
                    self.driver.implicitly_wait(10)
                    self.get_product_links()
                else:
                    self.driver.implicitly_wait(10)
                    self.actions.move_to_element(self.load_more_button)
                    self.load_more_button.click()
                    self.driver.implicitly_wait(5)
            return print(self.load_more_button.get_attribute("automationTrack"))

        # Collects the data from the each of the collected links(product code, sale price etc.)
        def get_product_data(self):
            self.num_clothing_items = len(self.shop_link_list)
            for i in tqdm(range(self.num_clothing_items), 'Collecting Data from Links'):
                self.driver.implicitly_wait(10)
                self.driver.get(self.shop_link_list[i])
                time.sleep(5)

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
                    self.full_item_list['product_id'].append('None')

                # Collects the image source for each of the product to download in get_images() function
                try:
                    image = self.driver.find_element_by_xpath('//img[@class="gallery-image"]')
                    image_src = image.get_attribute('src')
                    self.full_item_list['image'].append(image_src)
                    self.imagesrc_list.append(image_src)

                except NoSuchElementException:
                    self.full_item_list['image'].append('None')

                #Collects the product name of each of the items
                try:
                    product_header = self.driver.find_element_by_xpath('//div[@class="product-hero"]')
                    product_name = product_header.find_element_by_xpath('./h1').text.strip()
                    self.full_item_list['product_name'].append(product_name)
                except NoSuchElementException:
                    self.full_item_list['product_name'].append('None')

                #Collects the market price for each of the products
                try:
                    previous_price = self.driver.find_element_by_xpath('//span[@data-id ="rrp-price"]').text.strip()
                    previous_price = previous_price.replace('RRP', '')

                    #Some of the website use the RRP tag and other used a previous_price tag
                    if previous_price == '':
                        previous_price = self.driver.find_element_by_xpath(('//span[@data-id ="previous-price"]')).text.strip()
                        previous_price = previous_price.replace('Was', '')
                    self.full_item_list['previous_price'].append(previous_price)
                except NoSuchElementException:
                    self.full_item_list['previous_price'].append('None')

                # Collects the sale price of each of the products
                try:
                    sale_price = self.driver.find_element_by_xpath('//span[@data-id="current-price"]').text.strip()
                    sale_price = sale_price.replace("Now", '')
                    self.full_item_list['sale_price'].append(sale_price)
                except NoSuchElementException:
                    self.full_item_list['sale_price'].append('None')

                # Collects the percentage difference between market and sale price of products
                try:
                    sale_percentage = self.driver.find_element_by_xpath('//span[@class="product-discount-percent"]').text.strip()
                    self.full_item_list['sale_percentage'].append(sale_percentage)
                except NoSuchElementException:
                    self.full_item_list['sale_percentage'].append('None')

                # Collects the color of the items. Some have multiple colors
                try:
                    colour = self.driver.find_element_by_xpath('//span[@class="product-colour"]').text.strip()

                    # If there are multiple colors instead of sizes then they are accounted for below
                    if colour == '':
                        colour = self.driver.find_element_by_xpath('//div[@data-test-id="colour-size-select"]').text.strip()
                        colour = colour.replace("Please select from", "")
                        colour = colour.replace("colors", 'colors:')
                    self.full_item_list['color'].append(colour)
                except NoSuchElementException:
                    self.full_item_list['color'].append('None')

                # Collects product description for each of the product
                try:
                    description = self.driver.find_element_by_xpath('//div[@class = "product-description"]').text.strip()
                    ab_description = description.replace("PRODUCT DETAILS", "")
                    self.full_item_list['product_details'].append(ab_description)
                except NoSuchElementException:
                    self.full_item_list['product_details'].append('None')

                # Collects the sizes for each of the products
                try:
                    sizes = self.driver.find_element_by_xpath('//select[@data-id="sizeSelect"]').text.strip()
                    sizes = sizes.replace("Please select", "")
                    if sizes == '':
                        sizes = self.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/section[2]/div/div/div/div[3]/div[1]/p').text.strip()
                    self.full_item_list['sizes'].append(sizes)
                except NoSuchElementException:
                    self.full_item_list['sizes'].append('None')

                # Added to organize each item by their respective product id
                self.organized_data  = {self.product_id_num:{'name':[product_name], 'image':[image_src], 'previous_price':[previous_price], 'sale price':[sale_price],'sale_percentage':[sale_percentage], 'color':[colour], 'description':[ab_description], 'sizes':[sizes]}}
                print(self.full_item_list[i])
                self.full_product_data.append(self.organized_data)
            return self.full_item_list, self.full_product_data


        # Saves the data to either a json file or a pd Dataframe/csv for later    
        def save_data(self):
            index = ['product_id','product_name', 'image', 'previous_price', 'sale_price', 'sale_percentage' 'color', 'product_details', 'sizes']
            org_index = {'product_id':{'product_name', 'image', 'previous_price','sale_price','sale_percentage','color','product_details', 'sizes'}}

            with open('ASOS_data/ASOS_Women_data', 'w') as fp:
                json.dump(self.full_item_list, fp,  indent=4)

            with open('ASOS_data/ASOS_Women_Org_data', 'w') as fp:
                json.dump(self.full_product_data, fp,  indent=4)


            df1 = pd.DataFrame.from_dict(self.full_item_list) 
            df1.to_csv (r'ASOS_data/ASOS_Women_Data_csv', index = index, header=True)

            df2 = pd.DataFrame.from_dict(self.full_product_data) 
            df2.to_csv (r'ASOS_data/ASOS_Women__Org_Data_csv', index = org_index, header=True)

            if os.path.exists('ASOS_data/ASOS_Women_Data_csv','ASOS_data/ASOS_Women_Org_data' ):
                return True

        # Will download each of the images from their respective image sources for later
        def get_images(self):
            if not os.path.exists('ASOS_data/images'):
                    os.makedirs('ASOS_data/images')

            len_images = len(self.imagesrc_list)
            print(len_images)
            number = 1
            for i in tqdm(range(len_images), 'Downloading images'):
                id = self.full_item_list['product_id'][i]
                if self.full_item_list['product_id'][i] == '' or 'None':
                    id = number 
                image = self.imagesrc_list[i]
                if image == 'None':
                    pass
                urllib.request.urlretrieve(image, f"ASOS_data/images/ASOS_image_{id}.jpg")
                number +=1
                if os.path.exists(f"ASOS_data/images/ASOS_image_{id}.jpg"):
                    return True
                else:
                    return False



        # Final Function that calls all the functions above in the necessary order    
        def scrape_website(self):
            self.load_and_accept_cookies()
            self.load_more_products()
            self.get_product_links()
            self.get_product_data()
            self.save_data()
            self.get_images()
            self.driver.close()


# Begins the scraping process                
new_Scraper_ASOS= Scraper()
new_Scraper_ASOS.scrape_website() 
# %%
