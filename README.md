# Data Collection Pipeline - ASOS Sales Webpage

This project wil be used to illustrate how to use webscraping libraries to showcase the ability to create a Python class with all the necessary methods to collect data from the website including how to browse the website, how to extract data from the website, how to save the data to a database, etc.
_______________________________________________________________________________________________________________________________________________
## Milestone 1: Setting up Conda Environment and Web Driver (Completed)
 
 - For this webscraping project, Chrome Version (Version 101.0.4951.54) was downloaded for Ubuntu and will be used as the main browser for this webscraping project.

- The corresponding [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=101.0.4951.41/) (Version 101.0.4951.54) was then downloaded to be used as the main driver for the project.

- Next, a conda environment was set up with the necessary dependencies including `selenium`, `pip` and `ipykernel`. 

      # Setting up conda environment:
      conda create --name Data_Collection_Pipeline
      conda activate Data_Collection_Pipeline
      
      setup= (name = 'ASOS_data',
        version = 1.0,
        packages = find_packages(),
        install_requires = [
            beautifulsoup4==4.11.1,
                boto3==1.24.2,
                botocore==1.27.2,
                jsonschema==4.6.0,
                pandas==1.4.2,
                pip==22.2.2,
                prometheus_client==0.14.1,
                psycopg2==2.8.6,
                requests==2.28.0,
                s3transfer==0.6.0,
                selenium==4.3.0
                sqlalchemy==1.4.32,
                tqdm==4.64.0,
                urllib3==1.26.9,
                webdriver-manager==3.7.1,
                argparse-prompt])
     
------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 2: Creation of Scraper Class (Completed)
- First, `load_and_accept_cookies()`function was created to bypass cookies on the ASOS website:
  *An event listener was added for unit testing this function.
  
         def _load_and_accept_cookies(self):
              self.driver.implicitly_wait(10)
              accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
              self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True' );});",accept_cookies_button)
              accept_cookies_button.click()
              time.sleep(1)
              self.unit_Test_Cookies = accept_cookies_button.get_attribute("automationTrack")
              return self.unit_Test_Cookies

- TO navigate from the ASOS homepage, the `nav_to_sale_pg` function selects the options to navigate to the either the men or women sale website. This ensures the correct website will be scraped
       
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
  *An event listener was added for unit testing this function

- TO collect the amount of links from the site, it was necessary to scroll to the botton of the page and click 'load more' within the selenium driver. Therefore `load_more_product()` function was created for this purpose
    def _load_more_products(self):
           if self.n_pages == 0:
               self.unit_Test_Load_1 = 'True'

           while self.load_pages != self.n_pages:
               self.driver.implicitly_wait(10)
               load_more_button = self.driver.find_element(By.XPATH, '//a[@data-auto-id = "loadMoreProducts"]')
               self.actions.move_to_element(load_more_button)
               load_more_button.click()
               self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True');});",load_more_button)
               self.unit_Test_Load_1 = load_more_button.get_attribute("automationTrack")
               self.load_pages +=1
               time.sleep(1)

           if self.load_pages == self.n_pages:
               self.unit_loaded_pages = True

           return self.unit_loaded_pages, self.unit_Test_Load_1
   *An event listener was added for unit testing this function
                    
 - Next, ``get_product_links()`` function was made to collect links from the ASOS website:
    
        def _get_product_links(self):
            self.shop_link_list = []
            time.sleep(3)
            clothing_container = self.driver.find_element_by_xpath('//div[@class="_3pQmLlY"]')
            clothing_section = clothing_container.find_elements_by_xpath('./section')
            for section in clothing_section:
                article = section.find_elements_by_xpath('./article')
                time.sleep(3)
                for articles in article:
                    a_tag = articles.find_element_by_tag_name('a')
                    link = a_tag.get_attribute('href')
                    self.shop_link_list.append(link)

            # Confirms the necessary links have been collected       
            print(f'There are {len(self.shop_link_list)} links in this link list')
                    
- These results were saved in a list and the code was initialised with `if __name__ == "__main__" ` in a class so that it only runs if this file is run directly rather than on any import.

-------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 3: Collecting the Data and Images from the links (Completed)

- From each of the collected links, we collected the following data: 
                                       1)'product_id'
                                       2)'product_name',
                                       3)'image', 
                                       4)'previous_price', 
                                       5)'sale_price',
                                       6)'sale_percentage', 
                                       7)'color', 
                                       8)'product_details',
                                       9)'sizes' 
    using their respective xpath from the Male or Women Sale page on the ASOS website. 
    
    -   This part of the code also included code to bypass the 'student discount' popup
    -   Each page also had a 'show more' button' that was also pressed to expose all the necessary data
    -   This information was saved to `self.full_item_list` in a dictionary format
            


- Next a `save_data()` function was created to save the dictionaries to a json and csv file for future use and saved locally. 
        
        def _save_data(self):
        self.data_dir = str(os.getcwd())
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

  
  ![image](https://user-images.githubusercontent.com/102431019/185657865-6d611094-ef0e-4fee-a066-96697f9e9577.png)

 - Next. the `get_images()` function was created to download the images from the website on a local machine using the image source codes collecting from the `get_product_data()` functions using `urllib.requests`. A progress bar was also added using `tqdm` for easy visualisation.
   -Additionally, `ssl` was used to fix an error thrown my `urllib.requests`. 
 
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
                  self.test_image.append(False
      
 ![image](https://user-images.githubusercontent.com/102431019/185657948-89fb297f-1c05-4ae2-8edc-7eade3aec14b.png)
       
   ##### Pictured above is the files that were downloaded with the appropriate product code in the naming convention collected during unit testing
   
-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 4: Documentation and Testing (Complete)

- Each of the functions were then checked for redundancy and efficiency. 

- Docstrings were added for clear documentation on the purpose of each function (Example Pictured Below)
![image](https://user-images.githubusercontent.com/102431019/185658369-31c31af0-e7d8-436b-8fc6-cf4fed9b8e28.png)

- Unit test were created for each of the functions and then all unit test were run through `TestSuite.py`. 
   - `Data_Collection_Pipeline_small_batch_for_unit_testing` used only the first five products on the ASOS Women's Sale page as testing all 72   products on each page would be time consuming
   - All unit tests passed (Pictured Below)

![image](https://user-images.githubusercontent.com/102431019/173687105-26455b91-eaa2-4ca0-a1fc-525cebdcd3d3.png)

 
-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 5: Scalably Store the Data (Completed)

-Each record should have its own JSON file containing all information for that record and uploaded directly to S3 using boto3. This should include both the JSON and image data.To do this, `_s3_data_dump()` and `_s3_image_dump()` functions were created.
 
##### Pictured Below: The correspoding code to save and upload the necessary files to a created s3 bucket. 
![image](https://user-images.githubusercontent.com/102431019/185658860-19ebc049-c54a-4316-a719-b9af42a4dccd.png)


##### Pictured Below:This is an example of the uploaded files in the AWS S3 bucket including the uploaded images
![image](https://user-images.githubusercontent.com/102431019/185660696-de805b7d-2968-4596-a21c-8a0ce76c1e4c.png)


- A free tier micro RDS database was created to allow for the data to be uploaded to a postgres SQL server. As the website is scraped consecutively, this will allow one to sort and query the collected data.

![image](https://user-images.githubusercontent.com/102431019/185659256-3d045ea4-8d6f-4560-9e60-211d38304942.png)
##### Pictured Above: The corresponding code to upload the data to the Postgres SQL server via `sqlalchemy` and `psyopg2`

![image](https://user-images.githubusercontent.com/102431019/185661433-350ef350-5943-40b0-aba5-025384aa5ba6.png)
##### Pictured Above: A picture of the working Postgres SQL server with an example of the collected data from the Men's Sale Website


-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 6: Prevent Rescraping and Getting More Data (Completed)

- The scraper will be used to continuously collect data, functions needed to be built to  A) prevent rescraping the same data, B) retrieve previously scraped data, C) appended the data to previous files, and D )upload the new appended files. 

#### A) Preventing rescraping the same data -- Postgres-- TO prevent rescraping the same data, a QUERY was done to create two different tuples. We created two different Queries because some products do not have a `product_id` and therefore would need to be matched based on the `product_name`.
  
        def _previously_scraped(self):
             print("\n Let's check your SQL details...\n")
             try:
                 if self.sql_args.sql_password == None or self.sql_args.sql_endpoint==None:
                     self.get_sql_info()
                 else:
                     connection = psycopg2.connect( 
                     host = self.sql_args.sql_endpoint, # Change it for your AWS endpoint
                     user = self.sql_args.sql_user,
                     password = self.sql_args.sql_password,
                     port = self.sql_args.sql_port,
                     dbname =self.sql_args.sql_db_name)

                     cursor = connection.cursor()
                     cursor.execute(f'SELECT product_id, product_name, link, image from public."ASOS_{self.gender}_Data"')
                     self.duplicate_check = cursor.fetchall()
                     cursor.execute(f'SELECT product_name, link, image, sale_price, previous_price from public."ASOS_{self.gender}_Data"')
                     self.duplicate_check_2 = cursor.fetchall()
                     cursor.close()
                     connection.close()
                     print("Great! Your postgres connection was successful")

             except OperationalError:
                 print("\n Sorry. The sql connection was not able to be established. \n Please check your details below and try re-entering them now")
                 print(self.sql_args)
                 self._get_sql_info()
                 
- Additionally, once the queries were collected they were then compared to the product data being collected from the `_get_product_data()` functions.

          try:
                   scraped_entry_1 = (product_name, link, image_src, sale_price, previous_price)
                   scraped_entry_2 = (product_id_num, product_name, str(link), sale_price)
                   if self.previous == True and scraped_entry_2 in self.duplicate_check:
                       continue
                   elif self.previous == True and scraped_entry_1 in self.duplicate_check_2:
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
                   
                   
#### B) Retrieving previously scraped data -- AWS S3 Bucket -- To prevent the S3 bucket from rescraping the same data and allow for the files to be appended in later code. `_prev_data_retrieve()` function was added. 
  
       def _prev_data_retrieve(self):
            try:
                print('Lets try to connect to your S3 bucket...')
                self.data_dir = str(os.getcwd())
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

                print('\n Great! A connection to your S3 bucket was made successfully!')

           except:
               print("\n Sorry. A connection your S3 bucket was not able to be established. \n Please check your details below and try re-entering them now")
               print(self.aws_args)
               self._get_aws_info()
   
  - Each previous file with the selected gender would be downloaded and then deleted from the S3 bucket to avoid confusion and allow for the new files to be uploaded. 

 #### C) Appending Data from New Scrapes -- AWS S3 Bucket -- The previously scraped data and saved data was then converted to a dataframe and `pandas.concat` was used to merge the two dataframes. Additionally, the `pd.drop_duplicates()` function was also used to ensure there were not repeated entries. Finally, the files containing the individual dataframes were deleted and the new appended file was then saved as a csv or json file. 
 
     def _prev_data_append(self):
          os.chdir(self.previously_scraped_path)
          for files in os.listdir():
              if '.json' in files and 'Women' in files:
                  prev_data_scrape = pd.read_json(f'{files}')
                  updated_df = pd.concat([prev_data_scrape.reset_index(drop=True), 
                                self.products.reset_index(drop=True)], axis=0, join='inner',ignore_index=True)
                  updated_df = updated_df.drop_duplicates(subset =['product_id', 'product_name'], keep ='first')
                  os.remove(f'{files}')
                  updated_df.to_json(r'ASOS_Women_Data_Updated.json')


              elif '.csv' in files and 'Women' in files:
                  prev_data_scrape = pd.read_csv(f'{files}')
                  updated_df_2 = pd.concat([prev_data_scrape.reset_index(drop=True), 
                                self.products.reset_index(drop=True)], axis=0, join='inner',ignore_index=True)
                  updated_df_2 = updated_df_2.drop_duplicates(subset =['product_id', 'product_name'], keep ='first')
                  os.remove(f'{files}')
                  updated_df_2.to_csv(r'ASOS_Women_Data_Updated.csv')

              elif '.json' in files and 'Men' in files:
                  prev_data_scrape = pd.read_json(f'{files}')
                  updated_df = pd.concat([prev_data_scrape.reset_index(drop=True), 
                                self.products.reset_index(drop=True)], axis=0, join='inner',ignore_index=True)
                  updated_df = updated_df.drop_duplicates(subset =['product_id', 'product_name'], keep ='first')
                  os.remove(f'{files}')
                  updated_df.to_json(r'ASOS_Men_Data_Updated.json')

              elif '.csv' in files and 'Men' in files:
                  prev_data_scrape = pd.read_csv(f'{files}')
                  updated_df_2 = pd.concat([prev_data_scrape.reset_index(drop=True), 
                                self.products.reset_index(drop=True)], axis=0, join='inner',ignore_index=True)
                  updated_df_2 = updated_df_2.drop_duplicates(subset =['product_id', 'product_name'], keep ='first')
                  os.remove(f'{files}')
                  updated_df_2.to_csv(r'ASOS_Men_Data_Updated.csv')

          file_path = f'{self.data_dir}/ASOS_data'     
          os.chdir(file_path)
          for files in os.listdir():
              if '.csv' in files or '.json' in files:
                  os.remove(f'{files}')

 #### D) Uploading the appended files: The appended files were then uploaded using the previously shown `_s3_data_dump()` and `_s3_image_dump()` functions for AWS S3. The `_postgres_dump()` function was used to append the 'self.products' dataframe references in the `_save_data()` function because this dataframe had already been checked against the Postgres Database via `_previously_scraped()` function listed in A).

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 7: Making the Scraper User Friendly (Completed)

- Several functions were added to allow users to interact with the scraping program including the ability to select:
    - Whether to scrape the Men's or Women's ASOS Sale webpage
    ![image](https://user-images.githubusercontent.com/102431019/185668993-90c9fe8c-5639-43fd-8859-96efd96bece3.png)

    - How many products they would like to scrape
    ![image](https://user-images.githubusercontent.com/102431019/185669187-1b964dd8-1876-465c-aa31-bfc332ccbdfd.png)

    - Input their own AWS S3 and Postgres Database Information to append scraped data to their own S3 buckets and RDS Databases
    ![image](https://user-images.githubusercontent.com/102431019/185669316-e90ad991-fa9d-40e5-b858-b8d30b4fd488.png)

 - Pictured below: User friendly options were added using `argparse_prompt` and appear when running the program. 
    - Defaults were set based on the AWS S3 and Postgres setting set up for this project. However, users can enter their own information as             pictured. 
    - Both the Postgres SQL password and AWS_Secret_Access_Code were made secure and do not appear in the CLI. 
  ![image](https://user-images.githubusercontent.com/102431019/185671045-2d32f09a-6d86-4823-8a1e-a507ad4bd373.png)
     
   - If a connection was not able to be made to either AWS S3 Bucket or Postgres Database then an error will be thrown, all entered data              including the passwords will be printed and the user will be asked to re-enter their credentials. An example of this is pictured below:
   ![image](https://user-images.githubusercontent.com/102431019/185671464-cee87db5-9305-48fd-9e28-e7acbd6f3c99.png)


#### It is important to note the interactive options were not included in the file `Updated_ASOS_Cron.py` because this file contains a `Scraper()` class specifically designed to run with cronjobs in which 25 products from both the Men and Women Sale webpages will be collected every Friday. 
     
-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 8:Monitoring and Alerting (In Progress(See ISSUE))

 - In order to containerise the scraper program, the scraper program needed to be run in headless mode. This was completed by adding arguments to the `webdriver.ChromeOptions()` while running starting the driver. 
    
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
           options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
           options.add_argument("window-size=1920,1080")
           self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  
           self.driver.get(self.url)
           self.actions = ActionChains(self.driver)
           self.driver.implicitly_wait(10)

 - Next, a Dockerfile was created to build a Docker Image to allow one to :
    -  Choose a base image
    -  Put everything required by the scraper within the container
    -  Install any dependencies
    -  Run the main Python file
    
 ##### Pictured Below: In the left window is the requirement.txt file which list all the required dependencies and on the right is the Dockerfile used to build the docker images.
 ![image](https://user-images.githubusercontent.com/102431019/185673647-0343fba0-8932-438f-9cf0-01c26141a43c.png)

 ##### Pictured Below: The docker images that were created and containerised. 
 ![image](https://user-images.githubusercontent.com/102431019/185673941-98562e25-2a0d-4bde-83a3-0c352d41a27e.png)
 
 ##### Pictured Below: These images were then pushed to DockerHub
![image](https://user-images.githubusercontent.com/102431019/185675059-de43ee19-f1d8-4e95-9752-bcb5698cb2c7.png)


- An SSH connection was then established to connect to an EC2 Instance. 
    - A free tier EC2 instance was deployed through the AWS console
    - Using SSH Client in VS Code, a configuration file was edited to include the EC2 Instance details
    - Finally a connection was extablished through VS Code
    
- A `git clone` was then created within the SSH connection to copy the required files

- `sudo apt update` and `sudo apt upgrade` was run to allow for Docker to added to the SSH Connection

- `sudo apt install docker.io` was then used to install Docker 

- Docker images were then pulled from DockerHub. 

![image](https://user-images.githubusercontent.com/102431019/185676427-c7ea382c-8447-4197-ae9b-612cee24b3ec.png)
##### Picturd Above: In the left-hand corner in the explorer under HOME[SSH: ASOS], we can see the files that were cloned from github and the SSH files in the ubuntu dropdown corresponding to an open SSH connection. In the terminal window, the first command indicates the presence of the required Docker Images and the second command shows the Images run smoothly.

-The prometheus configuration file was then created and edited to allow one to observe metrics on the EC2 instance, the local machine and the docker containers (Pictured Below)
![image](https://user-images.githubusercontent.com/102431019/185679796-9efb7b40-203f-4772-a107-93c99f8bbbf1.png)

#### ISSUE : There was a problem getting the node explorer to work with my local machine but the other metrics were able to viewed successfully.
![image](https://user-images.githubusercontent.com/102431019/185680504-bef58bd8-4fd1-4886-87e3-2c3ad225e3a7.png)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 9:Setup CI/CD Pipeline for Docker Image (Completed)

-The final step was to create GitHub Actions to push updated versions of the scraper to DockerHub by creating the necessary Secrets. 
 -A GitHub action was created to be triggered on a push to the main branch of your repository.The action builds the Docker image and pushes it to my Dockerhub accoun (Pictured Below)
 ![image](https://user-images.githubusercontent.com/102431019/185682475-056b50c9-cc54-4219-aef6-f7e5f40fb54f.png)

 
-Cronjobs were then added to run the scraper every Friday at Midnight. The cronjobs stops and kill the container, as well as pulls the latest image from your Dockerhub account (Pictured Below).
![image](https://user-images.githubusercontent.com/102431019/185682304-8f9c6c07-16f8-49e7-bfc4-99d87d205062.png)

------------------------------------------------------------------------------------------------------------------------------------------------------------
## Conclusions

Positives: I gained an in depth experience using `Selenium Webdriver`, `Docker`, `GitHub Actions`, `Grafana`, `Prometheus`, `Postgres`, `AWS S3`, `AWS RDS` and `AWS EC2` to build a working Data Collection Pipeline. It was a rewarding experience allowing me to achieve a working knowledge of several important programs that are widely used within the Data Science/Data Engineering Industry. 

Future Goals: I would like to build another Data Collection Pipeline based on my interest in the scientific field. An example would be to use the UniProt or RCSB Databases to build a Data Collection Pipeline for proteins involved in specific diseases as I think this could be useful and challenging. 

Problem Solving: In terms of the programming, I would end the day with my scraper working and then try to run it a few days later but minor changes were made to the website resulting in having to make the necessary changes to the base code. Secondly, the hardest challenge was getting the scraper to run in both the Docker container and EC2 instance as many of the interactive options did not work originally. Using `argparse_prompt` eliminated some of the challenges I faced with the in-built `argparse` functions because I did not need to worry about calling the required flags within the Docker container. `argparse_prompt` did not need flags and would prompt the user independently. I also ran into problems with the `credential.json` and using .gitignore and .dockerignore to ensure my credentials would not be uploaded. There were times were the `credential.json` file was not recognized in the file structure but this was fixed by using the full PATH location. Finally, I ran into a problem using the interactive items of y scraper with cronjobs as it would throw an error so, a second file `Updated_ASOS_Cron.py` was created for this specific purpose of running the scraper in a cronjob. 
 
