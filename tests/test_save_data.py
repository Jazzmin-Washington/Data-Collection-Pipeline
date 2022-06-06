#%%
# Unit Test for save_data function
import selenium
from selenium.webdriver import Chrome
import pandas as pd
import json
import os
import shutil
import unittest 
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS



class TestSaveData(unittest.TestCase):

    def setUpClass():
        ASOS.load_and_accept_cookies()
        ASOS.nav_to_sale_pg()
        ASOS.get_product_links()
        ASOS.get_product_data()
        ASOS.save_data()
    
    

    def test_saved_json_file_dict(self):
        self.path_1 = '/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline/ASOS_data/ASOS_Women_data.json'
        f = open (self.path_1, "r")
  
        # Reading from file
        data = json.load(f)
        print(data)
  
    # Iterating through the json list

        for i in range(len(data)):
            print(data['product_id'][i], ASOS.full_item_list['product_id'][i] )
            self.assertTrue(data['product_id'][i] == ASOS.full_item_list['product_id'][i], 'Product Code does not match saved data file')
            self.assertTrue(data['sale_price'][i] == ASOS.full_item_list['sale_price'][i], 'Sale Price does not match saved data file') 
            self.assertTrue(data['product_name'][i] == ASOS.full_item_list['product_name'][i], 'Product Name does not match saved data file')

            self.assertTrue(data['sizes'][i], ASOS.full_item_list['sizes'][i], "Sizes does not match saved data")
            self.assertTrue(data['color'][i], ASOS.full_product_data['color'][i], "Color data does not match saved data")
            self.asserTrue(data['sale_price'][i], ASOS.full_item_list['sale_price'][i], "Sale price does not match saved data")

  
    
    def test_csv_methods(self):

        self.path_3 = '/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline/ASOS_data/ASOS_Women_Data.csv'
        df1 = pd.read_csv(f'{self.path_3}')
        dict_1 = df1.to_dict()
        print(dict_1)

        self.assertDictEqual(ASOS.full_item_list, dict_1, 'CSV file was not able to be converted to a dictionary')
        

    def test_csv_and_json_saved(self):
         self.assertTrue(ASOS.saving_data == True, 'Both file types were not successfully saved') 

    

    def tearDownClass(): 
       ASOS.driver.quit()
        
if __name__ == '__main__':
    unittest.main()
