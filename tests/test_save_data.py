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



class TestFunction_6(unittest.TestCase):

    def setUpClass():
        new_scraper = ASOS
        ASOS._save_data()
    
    def test_saved_json_file_dict(self):
        self.path_1 = '/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline/ASOS_data/ASOS_Women_data.json'
        f = open (self.path_1, "r")
  
        # Reading from file
        data = json.load(f)
  
    # Iterating through the json list

        for i in range(5):
        
            self.assertEqual(data['product_id'][i], ASOS.full_item_list['product_id'][i], 'Product Code does not match saved data file')
            self.assertEqual(data['sale_price'][i], ASOS.full_item_list['sale_price'][i], 'Sale Price does not match saved data file') 
            self.assertEqual(data['product_name'][i],  ASOS.full_item_list['product_name'][i], 'Product Name does not match saved data file')
            self.assertEqual(data['sizes'][i], ASOS.full_item_list['sizes'][i], "Sizes does not match saved data")
            self.assertEqual(data['color'][i], ASOS.full_item_list['color'][i], "Color data does not match saved data")
            self.assertEqual(data['sale_price'][i], ASOS.full_item_list['sale_price'][i], "Sale price does not match saved data")

        f.close()
    
    def test_csv_methods(self):

        self.path_3 = '/home/jazz/Documents/AiCore_Projects/Data_Collection_Pipeline/Data-Collection-Pipeline/ASOS_data/ASOS_Women_Data.csv'
        df1 = pd.read_csv(f'{self.path_3}', sep=',', header=0, index_col = 0).to_dict('list')

        self.assertDictEqual(ASOS.full_item_list, df1, 'CSV file was not able to be converted to a dictionary')
        

    def test_csv_and_json_saved(self):
         self.assertTrue(ASOS.saving_data == True, 'Both file types were not successfully saved') 


    def tearDownClass(): 
       print('\n Product Data completed')
      
        
if __name__ == '__main__':
    unittest.main()

