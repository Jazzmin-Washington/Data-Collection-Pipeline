# Data Collection Pipeline

This project wil be used to illustrate how to use webscraping libraries to showcase the ability to create a Python class with all the necessary methods to collect data from the website including how to browse the website, how to extract data from the website, how to save the data to a database, etc.
_______________________________________________________________________________________________________________________________________________
## Milestone 1: Setting up Conda Environment and Web Driver (Completed)
 
 - For this webscraping project, Chrome Version (Version 101.0.4951.54) was downloaded for Ubuntu and will be used as the main browser for this webscraping project.

- The corresponding [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=101.0.4951.41/) (Version 101.0.4951.54) was then downloaded to be used as the main driver for the project.

- Next, a conda environment was set up with the necessary dependencies including `selenium`, `pip` and `ipykernel`. 

      # Setting up conda environment:
      conda create --name Data_Collection_Pipeline
      conda activte Data_Collection_Pipeline
      
      conda install pip
      conda install selenium
      conda install ipykernel
      conda install BeautifulSoup4
      conda install Pandas
      conda install tqdm
      
     
------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 2: Creation of Scraper Class (Completed)
- First, `load_and_accept_cookies()`function was created to bypass cookies on the ASOS website:
     
       def load_and_accept_cookies(self):
            self.driver.implicitly_wait(10)
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')))
            accept_cookies_button.click()
            time.sleep(2)

- TO colect a healthy amount of links from the site, it was necessary to scroll to the botton of the page and click 'load more' within the selenium driver. Therefore `load_more_product()` function was created for this purpose

      def load_more_products(self):
                for i in range(6):
                    self.driver.implicitly_wait(10)
                    self.load_more_button = self.driver.find_element_by_xpath('//a[@data-auto-id = "loadMoreProducts"]')
                    self.actions.move_to_element(self.load_more_button)
                    self.driver.implicitly_wait(10)
                    if self.load_pages == 0:
                        self.actions.move_to_element(self.load_more_button)
                        self.load_more_button.click()
                        self.driver.implicitly_wait(10)
                        self.load_pages +=1
                    elif self.load_pages == self.n_pages:
                        self.driver.implicitly_wait(10)
                        self.get_product_links()
                    else:
                        self.driver.implicitly_wait(10)
                        self.actions.move_to_element(self.load_more_button)
                        self.load_more_button.click()
                        self.driver.implicitly_wait(5)
                    
 - Next, ``get_product_links()`` function was made to collect links from the ASOS website:
    
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
            print(f'There are {len(self.shop_link_list)} in this link list')
                    
- These results were saved in a list and the code was initialised with `if __name__ == "__main__" ` in a class so that it only runs if this file is run directly rather than on any import, and make sure it all works.

----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 3: Collecting the Data and Images from the links (Completed)

- From each of the collected links, we collected the following data: 'product_id','product_name', 'image', 'previous_price', 'sale_price','sale_percentage', 'color', 'product_details', and 'sizes' using their respective xpath from the Women's Sale - ASOS website. 
                   -   This is the lengthiest part of the code so it will not be included but please see Data_Collection_ASOS_v6.py file.
                   -   This part of the code also included code to bypass the 'student discount' popup
                   -   Each page also had a 'show more' button' that was also pressed to expose all the necessary data
                   -   This information was saved to a dictionaries: 
                           1) `self.full_item_list` containing the raw data, and
                           2) `self.full_product_data` organized by product code


- Next a `save_data()` function was created to save the dictionaries to a json and csv file for future use and saved locally. They have also been uploaded to the github account for review.

         def save_data(self):
            index = ['product_id','product_name', 'image', 'previous_price', 'sale_price', 'sale_percentage' 'color', 'product_details', 'sizes']
            org_index = {'product_id':{'product_name', 'image', 'previous_price','sale_price','sale_percentage','color','product_details', 'sizes'}}
            _price', 'sale_price', 'col
            with open('ASOS_data/ASOS_Women_data', 'w') as fp:
                json.dump(self.full_item_list, fp,  indent=4)
                
            
            with open("ASOS_data/ASOS_Women_Org_Data", 'w') as fp:
                json.dump(self.full_product_data, fp,  indent=4)
                
            df1 = pd.DataFrame.from_dict(self.full_item_list) 
            df1.to_csv (r'ASOS_data/ASOS_Women_Data_csv', index = index, header=True)
            
            df2 = pd.DataFrame.from_dict(self.full_product_data) 
            df2.to_csv (r'ASOS_data/ASOS_Women__Org_Data_csv', index = org_index, header=True)
  
  ![image](https://user-images.githubusercontent.com/102431019/170530796-a5833e98-a1db-4aa5-aa37-d3fce882b250.png)

 
 - Next. the `get_images()` function was created to download the images from the website on a local machine using the image source codes collecting from the `get_product_data()` functions using `urllib.requests`. A progress bar was also added using `tqdm` for easy visualisation.
 
        def get_images(self):
            print(self.imagesrc_list)
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
      
      ![image](https://user-images.githubusercontent.com/102431019/170530918-b17259cc-b27c-49ad-adb1-0ac3dca066fa.png)
       
     Pictured above is the files that were downloaded with the appropriate product code in the naming convention
-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 4: Documentation and Testing (In_Progress)

- Each of the functions were then checked for redundancy and efficiency. 
- Docstrings were added for clear documentation
- Unit test were created for each of the functions


-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 5: Scalably Store the Data (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 6: Scalably Store the Data (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 7: Get More Data (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 8:Monitoring and Alerting (Not Completed)

-----------------------------------------------------------------------------------------------------------------------------------------------------------
## Milestone 9:Setup CI/CD Pipeline for Docker Image (Not Completed)
