# Data Collection Pipeline

This project wil be used to illustrate how to use webscraping libraries to showcase the ability to create a Python class with all the necessary methods to collect data from the website including how to browse the website, how to extract data from the website, how to save the data to a database, etc.
_______________________________________________________________________________________________________________________________________________
## Milestone 1: Setting up Conda Environment and Web Driver (Completed)
 
 - For this webscraping project, Chrome Version (Version 101.0.4951.54) was downloaded for Ubuntu and will be used as the main browser for this webscraping project.

- The corresponding [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=101.0.4951.41/) (Version 101.0.4951.54) was then downloaded to be used as the main driver for the project.

- Next, a conda environment was set up with the necessary dependencies including `selenium`, `pip` and `ipykernel`. 

      # Setting up conda environment:
      conda create --name Data_Collection_Pipeline
      conda activate Data_Collection_Pipeline
      
      conda install pip
      conda install selenium
      conda install ipykernel
      conda install BeautifulSoup4
      conda install Pandas
      conda install tqdm
      
     
------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 2: Creation of Scraper Class (Completed)
- First, `load_and_accept_cookies()`function was created to bypass cookies on the ASOS website:
     
        def _load_and_accept_cookies(self):
        self.driver.implicitly_wait(10)
        accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
        self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 'True' );});",accept_cookies_button)
        accept_cookies_button.click()
        time.sleep(2)
        self.unit_Test_Cookies = accept_cookies_button.get_attribute("automationTrack")
        return self.unit_Test_Cookies
        
  *An event listener was added for unit testing this function

- TO navigate from the ASOS homepage, the `nav_to_sale_pg` function selects the options to navigate to the women's sale website. This ensures the correct website will be scraped.
        
        def _nav_to_sale_pg(self):
          self.driver.maximize_window()
          time.sleep(2)
          sales_button = self.driver.find_element_by_xpath('//button[@data-id="57242f2c-d207-471c-95b1-31d6839df360"]')
          view_all_button = self.driver.find_element_by_xpath('//a[@class="_1cjL45H _2Y7IAa_ CLdGn9X _1XjY6Zd _1zz7j1l"]')
          self.driver.implicitly_wait(10)
          self.actions.move_to_element(sales_button).click_and_hold().perform()
          self.driver.implicitly_wait(10)
          self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack', 
          'True' );});", view_all_button)
          view_all_button.click()
          self.driver.implicitly_wait(10)

*An event listener was added for unit testing this function

- TO collect a healthy amount of links from the site, it was necessary to scroll to the botton of the page and click 'load more' within the selenium driver. Therefore `load_more_product()` function was created for this purpose

        def _load_more_products(self):
        
            while self.load_pages != self.n_pages:
                self.driver.implicitly_wait(10)
                load_more_button = self.driver.find_element_by_xpath('//a[@data-auto-id = "loadMoreProducts"]')
                self.actions.move_to_element(load_more_button)
                load_more_button.click()
                self.driver.execute_script("var ele = arguments[0];ele.addEventListener('click', 
                function() {ele.setAttribute('automationTrack', 'True');});",load_more_button)
                self.unit_Test_Load_1 = load_more_button.get_attribute("automationTrack")
                self.driver.implicitly_wait(10)
                self.load_pages +=1

            if self.load_pages == self.n_pages:
                self.unit_loaded_pages = True
                time.sleep(2)

            return self.unit_loaded_pages, self.unit_Test_Load_1, self.n_pages, self.load_pages

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
                    
- These results were saved in a list and the code was initialised with `if __name__ == "__main__" ` in a class so that it only runs if this file is run directly rather than on any import, and make sure it all works.

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
    using their respective xpath from the Women's Sale - ASOS website. 
    
    -   This is the lengthiest part of the code so it will not be included but please see Data_Collection_ASOS_v6.py file.
    -   This part of the code also included code to bypass the 'student discount' popup
    -   Each page also had a 'show more' button' that was also pressed to expose all the necessary data
    -   This information was saved to a dictionaries: 
             1) `self.full_item_list` containing the raw data, and
             2) `self.full_product_data` organized by product code


- Next a `save_data()` function was created to save the dictionaries to a json and csv file for future use and saved locally. They have also been uploaded to the github account for review.

         def _save_data(self):
              index = ['product_id',
                      'product_name',
                      'image', 
                      'previous_price', 
                      'sale_price', 
                      'sale_percentage',
                      'color', 
                      'product_details', 
                      'sizes']


              save_path = '/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline'
              if not os.path.exists(f'{save_path}/ASOS_data'):
                      os.makedirs(f'{save_path}/ASOS_data')

              with open(f'{save_path}/ASOS_data/ASOS_Women_data.json', 'w+') as fp:
                  json.dump(self.full_item_list, fp,  indent=4)

              with open(f'{save_path}/ASOS_data/ASOS_Women_Org_data.json', 'w+') as fp:
                  json.dump(self.full_product_data, fp,  indent=4)


              df1 = pd.DataFrame.from_dict(self.full_item_list) 
              df1.to_csv(r'/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline/ASOS_data/ASOS_Women_Data.csv', 
              index = index, header=True)


              if os.path.exists(f'{save_path}/ASOS_data/ASOS_Women_Data.csv') and os.path.exists(f'{save_path}/ASOS_data/ASOS_Women_Org_data.json'):
                  self.saving_data = True
                  return self.saving_data, save_path

  
  ![image](https://user-images.githubusercontent.com/102431019/173680595-dddcf11d-9571-4fe0-b945-f27059c20f5b.png)

 - Next. the `get_images()` function was created to download the images from the website on a local machine using the image source codes collecting from the `get_product_data()` functions using `urllib.requests`. A progress bar was also added using `tqdm` for easy visualisation.
  -Additionally, `ssl` was used to fix an error thrown my `urllib.requests`. 
 
         def _get_images(self):
        save_path = '/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline'
        if not os.path.exists(f'{save_path}/ASOS_data/images'):
                os.makedirs(f'{save_path}/ASOS_data/images')

        self.test_images = []
        len_images = len(self.imagesrc_list)
        for i in tqdm(range(len_images), 'Downloading images'):
            id = self.full_item_list['product_id'][i] 
            image = self.imagesrc_list[i]
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(image, f"{save_path}/ASOS_data/images/ASOS_image_{id}.jpg")
            if os.path.exists(f"{save_path}/ASOS_data/images/ASOS_image_{id}.jpg"):
                self.test_images.append(True)
            else:
                self.test_image.append(False)
      
   ![image](https://user-images.githubusercontent.com/102431019/173680969-b3173072-4272-47a1-b49e-43cbd8211427.png)
       
   Pictured above is the files that were downloaded with the appropriate product code in the naming convention collected during unit testing
   
-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 4: Documentation and Testing (Complete)

- Each of the functions were then checked for redundancy and efficiency. 

- Docstrings were added for clear documentation on the purpose of each function (Example Pictured Below)
![image](https://user-images.githubusercontent.com/102431019/173681198-2378598f-687b-4a8b-8323-5747cdb1085d.png)

- Unit test were created for each of the functions and then all unit test were run through `TestSuite.py`. 
   - `Data_Collection_Pipeline_small_batch_for_unit_testing` used only the first five products on the ASOS Women's Sale page as testing all 72   products on each page would be time consuming
   - All unit tests passed (Pictured Below)

![image](https://user-images.githubusercontent.com/102431019/173687105-26455b91-eaa2-4ca0-a1fc-525cebdcd3d3.png)

 
-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 5: Scalably Store the Data (In Progress)

-Each record should have its own JSON file containing all information for that record and uploaded directly to S3 using boto3. This should include both the JSON and image data.

-Create a free tier micro RDS database, remember to make it publicly available. You can use pandas to create a dataframe for each record and then upload to RDS using psycopg2 and sqlalchemy.

- Create a method which dumps the data directly to S3 using boto3.



-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 6: Scalably Store the Data (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 7: Get More Data (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 8:Monitoring and Alerting (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 9:Setup CI/CD Pipeline for Docker Image (Not Completed)
