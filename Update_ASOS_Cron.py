#%%
# Updating previous scrapes for Cronberg
import selenium
import pandas as pd
import json
import uuid
import os
import time
import ssl
import psycopg2
import sqlalchemy
import urllib.request
import boto3
import botocore.exceptions
import warnings
import math as math
from re import sub
from decimal import Decimal
from botocore.exceptions import ClientError
from botocore.exceptions import ConnectionError
from botocore.exceptions import InvalidEndpointConfigurationError
from botocore.exceptions import CredentialRetrievalError
from pandas import concat
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine
from psycopg2 import OperationalError
from argparse_prompt import PromptParser 
from urllib.error import ContentTooShortError
from tqdm import tqdm
from os.path import exists
from ASOS_Scraper import First_Scrape
warnings.filterwarnings("ignore", category=DeprecationWarning)



class Scraper():
    ''' Variables that were initialised including necessary lists, drivers and dictionaries
        These variables are used multiple times throughout several functions''' 
    def __init__(self):
        self.full_item_list = []
        self.load_pages = 0
        self.delay = 10
        self.data_dir = str(os.getcwd())
        

    ''' The _choose_gender_and_pages allows for users to select whether they would like 
    to scrape the Men's or Women's Sale Page. Additionally, it allows the user to select how many pages of
    products they would like to scrape. Each page containes of 72 products'''
        
    def _choose_gender_and_pages(self):
        if gender == 'M'or gender == 'm':
            self.gender = 'Men'
            self.url = 'https://www.asos.com/men/'
        elif gender == 'W' or gender =='w':
            self.gender ='Women'
            self.url = 'https://www.asos.com/women'
        else: 
            print("That's an invalid entry. Please enter either 'W' or 'M'")
            self._choose_gender_and_pages()




    ''' The _get_aws_info  and _get_sql_info functions were added for password protection and to allow the user to
     upload to their personal S3 buckets and SQL database. This allows for robust use'''
        
    def _get_credentials(self):
        self.aws_access_key_id = credentials["AWS_ID"]
        self.aws_secret_access_key = credentials["AWS_ACCESS_KEY"]
        self.aws_bucket = credentials["AWS_BUCKET"]
        self.aws_key =credentials["AWS_BUCKET_KEY"]
        self.sql_db_type = 'postgresql'
        self.sql_db_name ='postgres'
        self.sql_dbapi = 'psycopg2'
        self.sql_endpoint = credentials["RDS_ENDPOINT"]
        self.sql_user ='postgres'
        self.sql_password = credentials["RDS_PASS"]
        self.sql_port =5432

        self.s3 = boto3.client('s3',
        aws_access_key_id= self.aws_access_key_id,
        aws_secret_access_key= self.aws_secret_access_key)
        self.BUCKET = self.aws_bucket
        self.KEY = self.aws_key

    ''' The _previousl_scraped function connects to the users SQL Database that contains previous scrapes that you would like the current
    scrape to be appended to. It also ensures the products are not scraped twice making for cleaner data'''
            
    def _previously_scraped(self):
        connection = psycopg2.connect( 
        host = self.sql_endpoint, # Change it for your AWS endpoint
        user = self.sql_user,
        password = self.sql_password,
        port = self.sql_port,
        dbname =self.sql_db_name)

        cursor = connection.cursor()
        cursor.execute(f'SELECT product_id, product_name, link, image from public."ASOS_{self.gender}_Data"')
        self.duplicate_check = cursor.fetchall()
        cursor.execute(f'SELECT product_name, link, image, sale_price, previous_price from public."ASOS_{self.gender}_Data"')
        self.duplicate_check_2 = cursor.fetchall()
        cursor.close()
        connection.close()
        print(" Great! Your postgres connection was successful")


    def _prev_data_retrieve(self):
        self.previously_scraped_path = f'{self.data_dir}/previously_scraped'
        if not os.path.exists(f'{self.previously_scraped_path}'):
                os.makedirs(f'{self.previously_scraped_path}', exist_ok=True)

        paginator = self.s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.BUCKET, Prefix = self.KEY)

        for page in pages:
            for obj in page['Contents']:
                if '.json' in obj['Key'] and self.gender in obj['Key']:
                    file_key = obj['Key']
                    self.s3.download_file(self.BUCKET, file_key,f'{self.previously_scraped_path}/ASOS_{self.gender}_Data.json')
                    self.s3.delete_object(Bucket =self.BUCKET, Key = file_key)
    
                elif '.csv' in obj['Key'] and self.gender in obj['Key']:
                    file_key = obj['Key']
                    self.s3.download_file(self.BUCKET, file_key, f'{self.previously_scraped_path}/ASOS_{self.gender}_Data.csv')
                    self.s3.delete_object(Bucket =self.BUCKET, Key = file_key)
        print('\n Great! A connection to your S3 bucket was successful')
                        
        

    ''' The _start_drive function will start the selenium driver. If this is run before collecting the necessary data such as the aws_info and sq_info
    then it can cause issues. This allows the user to control when the driver is engaged. '''   
    
    
    def _start_driver(self):
        chrome_options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized") # open Browser in maximized mode
        options.add_argument("disable-infobars")# disabling infobars
        options.add_argument("--disable-extensions"); # disabling extensions
        options.add_argument("--no-sandbox") 
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox") 
        options.add_argument('--disable-gpu')      
        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005 Safari/537.36'")
        options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  
        self.driver.get(self.url)
        self.actions = ActionChains(self.driver)
        self.driver.implicitly_wait(10)

    ''' The load_and accept_cookies function clicks the accept cookies button 
     on the webpage using the selenium driver.
        
        An event listener was  added for unit testing'''

    def _load_and_accept_cookies(self):
        self.driver.implicitly_wait(10)
        accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
        self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True' );});",accept_cookies_button)
        accept_cookies_button.click()
        time.sleep(1)
        self.unit_Test_Cookies = accept_cookies_button.get_attribute("automationTrack")
        return self.unit_Test_Cookies

    ''' The nav_to_sale function is used to navigate to the women's sale webpage from the ASOS homepage
        An event listener was added for unit testing. ''' 

    def _nav_to_sale_pg(self):
        try:
            self.driver.maximize_window()
            time.sleep(2)
            if self.gender=='Women':
                sales_button = self.driver.find_element(By.XPATH, '//button[@data-id="57242f2c-d207-471c-95b1-31d6839df360"]')
                view_all_button = self.driver.find_element(By.XPATH, '//a[@class="_1cjL45H _2Y7IAa_ CLdGn9X _1XjY6Zd _1zz7j1l"]')
            elif self.gender=='Men':
                sales_button = self.driver.find_element(By.XPATH, '//button[@data-id="c223e1a9-dc0f-42f5-afca-5cf5988c716b"]')
                view_all_button = self.driver.find_element(By.XPATH, '//*[@id="c223e1a9-dc0f-42f5-afca-5cf5988c716b"]/div/div[2]/ul/li[1]/ul/li[1]/a')
                                                                
            self.driver.implicitly_wait(10)
            self.actions.move_to_element(sales_button).click_and_hold().perform()
            self.driver.implicitly_wait(10)
            self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True' );});", view_all_button)
            view_all_button.click()
            self.driver.implicitly_wait(10)
        except ElementNotInteractableException:
            self._nav_to_sale_pg()
   
    

    ''' The get_product_link function collects the links on the loaded products on the webpage and 
        appends them to a list for use in later functions '''

    def _get_product_links(self):
        self.shop_link_list = []
        self.driver.implicitly_wait(10)
        clothing_container = self.driver.find_element(By.XPATH, '//div[@data-auto-id="productList"]')
        clothing_section = clothing_container.find_elements(By.XPATH, './section')
        for section in clothing_section:
            article = section.find_elements(By.XPATH, './article')
            time.sleep(2)
            for articles in article:
                a_tag = articles.find_element(By.TAG_NAME, 'a')
                link = a_tag.get_attribute('href')
                self.shop_link_list.append(link)
        
    ''' The get_product_data collects the data from the each of the collected links including
        product code or uuid number if no product code/id is listed,
        image source for the products,
        name of the products,
        previous listed price,
        current sale price, 
        percentage difference between previous and sale prices,
        color of product,
        sizes of products (if statements were added for non-clothing products)
        and product description.
        
        
        To display all information that was collected, a show_more_button and pop_up button variables
        were also added'''   
        
    def _get_product_data(self):
        for i in tqdm(range(10), 'Collecting Data from Links'):
            link = self.shop_link_list[i]
            self.driver.implicitly_wait(5)
            self.driver.get(link)
            time.sleep(2)
    
            uuid_num = str(uuid.uuid4())
            uuid_num = uuid_num[:8]

            # Selects the "X" on the 'student discount' popup
            try:
                self.driver.implicitly_wait(5)
                popup = self.driver.find_element(By.XPATH, '//*[@id="att_lightbox_close"]')
                popup.click()
            except (ElementNotInteractableException, NoSuchElementException):
                pass
            
             # Selects the show more button to expose the relevant data for scraping  
            try:
                self.driver.implicitly_wait(5)
                self.show_more_button = self.driver.find_element(By.XPATH, '//div[@class="show-more"]')
                self.actions.move_to_element(self.show_more_button)
                self.show_more_button.click()
                
            except NoSuchElementException:
                pass
           
            try:
                show_details_button = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                '//div[@id="productDescriptionDetails"]')))
            except (NoSuchElementException,TimeoutException):
                try:
                    self.show_details = self.driver.find_element(By.XPATH, '//button[@class="DuCNB"]')
                    self.actions.move_to_element(self.show_details)
                    self.show_details.click()
                except (NoSuchElementException, ElementNotInteractableException):
                    pass
           
           
            # Collects the product id for each of the products
            try:
                product_id = self.driver.find_element(By.XPATH, '//div[@class="product-code"]')
                product_id_num = product_id.find_element(By.XPATH, './p').text
                if product_id_num == '' or product_id_num == 'None':
                    product_id_num = self.driver.find_element(By.XPATH, '//p[@class="Jk9Oz"]').text
                    product_id_num = product_id_num.replace('Product Code: ', '')
            except NoSuchElementException:
                try:
                    product_id_num = self.driver.find_element(By.XPATH, '//p[@class="Jk9Oz"]').text
                    product_id_num = product_id_num.replace('Product Code: ', '')
                except NoSuchElementException:
                    product_id_num = 'None'
                
            # Collects the image source for each of the product to download in get_images() function
            try:
                    image = self.driver.find_element(By.XPATH, '//img[@class="img"]')
                    image_src = image.get_attribute('src')  
            except NoSuchElementException:
                image_src= 'None'
            
            #Collects the product name of each of the items
            try:
                product_header = self.driver.find_element(By.XPATH, '//div[@class="product-hero"]')
                product_name = product_header.find_element(By.XPATH, './h1').text.strip()
            except NoSuchElementException:
                try:
                    product_name = self.driver.find_element(By.XPATH, '//h1[@class="jcdpl"]').text.strip()
                except NoSuchElementException:
                    product_name = 'None'
            
            
            #Collects the market price for each of the products
            try:
                previous_price = self.driver.find_element(By.XPATH, ('//span[@data-test-id ="previous-price"]')).text.strip()
                previous_price = previous_price.replace('Was', '')
                previous_price = previous_price.replace('RRP ', '')  
                if previous_price == "":
                    previous_price = self.driver.find_element(By.XPATH, '//span[@data-id ="rrp-price"]').text.strip()
                    previous_price = previous_price.replace('RRP ', '')     
            except NoSuchElementException:
                previous_price = self.driver.find_element(By.XPATH, ('//span[@data-id ="previous-price"]')).text.strip()
                previous_price = previous_price.replace('Was', '')
                previous_price = previous_price.replace('RRP', '')
                if previous_price == "":
                    previous_price = self.driver.find_element(By.XPATH, '//span[@data-id ="rrp-price"]').text.strip()
                    previous_price = previous_price.replace('RRP ', '')  


            # Collects the sale price of each of the products
            try:
                sale_price = self.driver.find_element(By.XPATH, '//span[@data-test-id="current-price"]').text.strip()
                if sale_price == '' :
                    sale_price = 'Item is not on sale'
            except NoSuchElementException:
                try:
                    sale_price = self.driver.find_element(By.XPATH, '//span[@data-id="current-price"]').text.strip()
                except NoSuchElementException:
                    sale_price = 'None'
            
            # Collects the percentage difference between market and sale price of products
            try:
                sale_percentage = self.driver.find_element(By.XPATH, '//span[@data-test-id="percentage-discount"]').text.strip()
                if sale_percentage == '' :
                    sale_percentage = 'Item is not on sale'             
            except NoSuchElementException:
                try:
                    sale_percentage = self.driver.find_element(By.XPATH, '//span[@class="product-discount-percent"]').text.strip()
                except NoSuchElementException:
                    sale_percentage = 'None'
            # Collects the color of the items. Some have multiple colors
            try:
                colour = self.driver.find_element(By.XPATH, '//span[@class="product-colour"]').text.strip()
            
                # If there are multiple colors instead of sizes then they are accounted for below
        
                if colour == '':
                    colour = self.driver.find_element(By.XPATH, '//div[@data-test-id="colour-size-select"]').text.strip()
                    colour = colour.replace("Please select from", "")
                    colour = colour.replace("colors", 'colors:') 
            except NoSuchElementException:
                colour = 'None'

            # Collects product description for each of the product
            try:
                description = self.driver.find_element(By.XPATH, '//div[@class = "product-description"]').text.strip()
                ab_description = description.replace("PRODUCT DETAILS", "")
                if description == '' or description == 'None':
                     self.driver.implicitly_wait(5)
                     ab_description = self.driver.find_element(By.XPATH, '//div[@class="F_yfF"]').text.strip()
            except NoSuchElementException:
                try: 
                    ab_description = self.driver.find_element(By.XPATH, '//div[@class="F_yfF"]').text.strip()
                except NoSuchElementException:
                    ab_description = 'None'
            
            # Collects the sizes for each of the products
            try:
                sizes = self.driver.find_element(By.XPATH, '//select[@data-id="sizeSelect"]').text.strip()
                sizes = sizes.replace("Please select", "")
                    
            except NoSuchElementException:
                try:
                    sizes = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[3]/section[2]/div/div/div/div[3]/div[1]/p').text.strip()
                except NoSuchElementException:
                    sizes = self.driver.find_element(By.XPATH, '//span[@class="product-size"]')

           
            try:
                scraped_entry_1 = (product_name, link, image_src, sale_price, previous_price)
                scraped_entry_2 = (product_id_num, product_name, str(link), sale_price)
                if scraped_entry_2 in self.duplicate_check:
                    continue
                elif scraped_entry_1 in self.duplicate_check_2:
                    continue
                else:
                    products = True
            except NameError:
                products =True
            
            if products == True:
                product = {
                    'uuid': uuid_num,
                    'product_id': product_id_num,
                    'product_name':product_name, 
                    'image': image_src,
                    'previous_price':previous_price, 
                    'sale_price': sale_price, 
                    'sale_percentage':sale_percentage, 
                    'color':colour, 
                    'product_details':ab_description, 
                    'sizes': sizes,
                    'link': link}
                    
                self.full_item_list.append(product)


    ''' The _save_data function is a private method that saves the data scraped from the respective webpage to a json and csv file for later use'''
   
    def _save_data(self):
        if not os.path.exists(f'{self.data_dir}/ASOS_data'):
                os.makedirs(f'{self.data_dir}/ASOS_data', exist_ok=True)
        os.chdir(f'{self.data_dir}/ASOS_data')
                
        self.products = pd.DataFrame.from_dict(self.full_item_list)
        
        if self.gender == 'Women':
            self.products.to_json(r'ASOS_Women_Data.json')
            self.products.to_csv(r'ASOS_Women_Data.csv') 


        elif self.gender == 'Men':
            self.products.to_json(r'ASOS_Men_Data.json')
            self.products.to_csv(r'ASOS_Men_Data.csv')
            
        
        if os.path.exists(f'{self.data_dir}/ASOS_data/ASOS_{self.gender}_Data.csv') and os.path.exists(f'{self.data_dir}/ASOS_data/ASOS_{self.gender}_Data.json'):
            self.saving_data = True
            return self.saving_data

    
    ''' As images of products are likely to change, each of the collected image source were used to
        download the images and saved locally for future reference. 

        Each photo was saved using their unique product id or uuid '''

    def _get_images(self):
        if not os.path.exists(f'{self.data_dir}/ASOS_data/images'):
            os.makedirs(f'{self.data_dir}/ASOS_data/images', exist_ok=True)
        os.chdir(f'{self.data_dir}/ASOS_data/images')

        self.test_images = []
        len_images = len(self.full_item_list)
        for i in tqdm(range(len_images), 'Downloading images'):
            id = self.full_item_list[i]['product_id'] 
            if id == '' or id == "None":
                id = self.full_item_list[i]['uuid'] 
            image = self.full_item_list[i]['image']
            if os.path.exists(f"{id}.jpg"):
                self.test_images.append(True)
                pass
            elif not os.path.exists(f"{id}.jpg"):
                ssl._create_default_https_context = ssl._create_unverified_context
                urllib.request.urlretrieve(image, f"{id}.jpg")
                self.test_images.append(True)
            else:
                self.test_image.append(False)
    
    
    '''The _prev_data_append allows the user to append the data scraped from the webpage to their files within the S3 Bucket in a neat manner'''

     def _prev_data_append(self):
        self.previously_scraped_path = f'{self.data_dir}/previously_scraped'
        os.chdir(self.previously_scraped_path)
        for files in os.listdir():
            if '.json' in files and self.gender in files:
                os.remove(f'{files}')

            elif '.csv' in files and 'Women' in files and self.gender == 'Women':
                prev_data_scrape = pd.read_csv(f'{files}')
                updated_df_2 = pd.concat([prev_data_scrape.reset_index(drop=True), 
                            self.products.reset_index(drop=True)], axis=0, join='inner',ignore_index=True)
                updated_df_2 = updated_df_2.drop_duplicates(subset =['product_id', 'product_name'], keep ='first')
                os.remove(f'{files}')
                updated_df_2.to_csv(r'ASOS_Women_Data_Updated.csv')
                updated_df_2.to_json(r'ASOS_Women_Data_Updated.json')
          

            elif '.csv' in files and self.gender in files:
                prev_data_scrape = pd.read_csv(f'{files}')
                updated_df_2 = pd.concat([prev_data_scrape.reset_index(drop=True), 
                            self.products.reset_index(drop=True)], axis=0, join='inner',ignore_index=True)
                updated_df_2 = updated_df_2.drop_duplicates(subset =['product_id', 'product_name'], keep ='first')
                os.remove(f'{files}')
                updated_df_2.to_csv(r'ASOS_Men_Data_Updated.csv')
                updated_df_2.to_json(r'ASOS_Men_Data_Updated.json')

        file_path = f'{self.data_dir}/ASOS_data'     
        os.chdir(file_path)
        for files in os.listdir():
            if '.csv' in files or '.json' in files:
                os.remove(f'{files}')

    ''' The _s3_data_dump and _s3_image_dump uploads the current data scraped and images collected 
        to their respective AWS S3 Bucket, As the image_source can change. It is good practice to download the images for 
        future comparisons'''

    def _s3_data_dump(self):
        print("\n Lets try to upload our appended files to your S3 Bucket")
        os.chdir(self.previously_scraped_path)
        for files in os.listdir():
            if '.csv' in files or '.json' in files:
                data_path = f'{self.previously_scraped_path}/{files}'
                file_key= f'{self.KEY}'+f'{files}'
                self.s3.upload_file(data_path, self.BUCKET, file_key)
                os.remove(f'{files}')

        print("\n Success! Uploading Images to AWS S3 Bucket...\n")
        self._s3_image_dump()

    def _s3_image_dump(self):
        os.chdir(f'{self.data_dir}/ASOS_data/images')
        file_path_2 = f'{self.data_dir}/ASOS_data/images'

        for images in os.listdir():

            if self.gender == 'Women':
                image_path = f'{file_path_2}/{images}'
                file_key_2 = f'{self.KEY}'+f'ASOS_Women_images/{images}'
                self.s3.upload_file(image_path, self.BUCKET, file_key_2)
                os.remove(f'{file_path_2}/{images}')
            elif self.gender == 'Men':
                image_path = f'{file_path_2}/{images}'
                file_key_2 = f'{self.KEY}'+f'ASOS_Men_images/{images}'
                self.s3.upload_file(image_path, self.BUCKET, file_key_2)
                os.remove(f'{file_path_2}/{images}')
        print("\n Images have been uploaded successfully\n")

    '''The postgres_dump will append the data to the user's SQL database which will allow them to be queried and organized in 
    an useful way for the user. In this function, this will also append the new scrape to the previous scrapes, as well'''

    def _postgres_dump(self):
        DATABASE_TYPE = self.sql_db_type
        DBAPI = self.sql_dbapi
        ENDPOINT = self.sql_endpoint
        USER = self.sql_user
        PASSWORD = self.sql_password
        PORT = self.sql_port
        DATABASE = self.sql_db_name
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")

        self.products.to_sql(f'ASOS_{self.gender}_Data', engine, if_exists='append', index=False)
        print("\n Data was successfully uploaded to your sql database \n")
    
    def _scrape_website(self):
        print("\n Thanks, Let's Begin Scraping! \n Spinning up webdriver...")
        self._start_driver()
        self._load_and_accept_cookies()
        print(' \n Cookies have been accepted ')
        self._nav_to_sale_pg()
        print(f"\n Webpage is now on the ASOS { self.gender}'s Sale Site ")
        self._get_product_links()
        print('\n All links from webpage have been collected.')
        print(f'\n Product Data for 50 products will now be collected\n ')
        self._get_product_data()
        print("\n Product Data has now been collected\n ")
        self._save_data()
        print('\n Data has been saved\n')
        self._get_images()
        print('\n Images have now been downloaded\n')
        self._quit_scraper()
         

           
    ''' The quit_scraper function will close the scraper once the data is collected and saved.'''
    def _quit_scraper(self):
        self.driver.quit()

Update_ASOS = Scraper()

if __name__ == "__main__": 
    Update_ASOS = Scraper()
    gender_list = ['M', 'W']
    cred=os.getcwd()
    credentials = pd.read_json(f'{cred}/scrapers/credentials.json', typ='dictionary')
    Update_ASOS._get_credentials()
    os.chdir(Update_ASOS.data_dir)
    for genders in gender_list:
        Update_ASOS.full_item_list = []
        gender = genders
        print(gender)
        Update_ASOS._choose_gender_and_pages()
        print(Update_ASOS.gender)
        Update_ASOS._prev_data_retrieve()
        Update_ASOS._previously_scraped()
        Update_ASOS._scrape_website()
        Update_ASOS._prev_data_append()
        Update_ASOS._s3_data_dump()
        Update_ASOS._postgres_dump()
        
        
     
