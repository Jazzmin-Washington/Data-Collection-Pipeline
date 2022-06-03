#%%  Unit Test for get_product_data function
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import json
import os
import unittest 
import shutil
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS


class TestSaveData(unittest.TestCase):

    def setUpClass():
        ASOS.save_data()
    

    def test_saved_json_file_dict(self):
        f = open ('/scrapers/ASOS_data/ASOS_Women_data.json', "r")
  
        # Reading from file
        data = json.load(f)
        print(data)
  
    # Iterating through the json list

        for i in range(len(data)):
            self.assertTrue(data['product_id'][i] == ASOS.full_item_list['product_id'][i], 'Product Code does not match saved data file')
            self.assertTrue(data['sale_price'][i] == ASOS.full_item_list['sale_price'][i], 'Sale Price does not match saved data file') 
            self.assertTrue(data['product_name'][i] == ASOS.full_item_list['product_name'][i], 'Product Name does not match saved data file')

        f.close()
    
    def test_saved_json_file_org_dict(self):
        fp = open ('scrapers/ASOS_data/ASOS_Women_Org_data.json', "r")
  
        # Reading from file
        org_data = json.load(fp)
        
    # Iterating through the json d
    # ict
       
        for i in range(len(org_data)):
            self.assertTrue(org_data[i]['sizes'] == ASOS.full_product_data[i]['sizes'], "Product Code does not match saved data")
            self.assertTrue(org_data[i]['color'] == ASOS.full_product_data[i]('color'), "Color data does not match saved data")
            self.asserTrue(org_data[i]['sale_price'] == ASOS.full_product_data[i]['sale_price'], "Sale price does not match saved data")

        fp.close() 
    
    def test_csv_methods(self):
        df1 = pd.read_csv(r'scrapers/ASOS_data/ASOS_Women_Data.csv')
        dict_1 = df1.to_dict()

        self.assertDictEqual(ASOS.full_item_list, dict_1, 'CSV file was not able to be converted to a dictionary')
        

    def test_csv_and_json_saved(self):
         self.assertTrue(ASOS.saving_data == True, 'Both file types were not successfully saved') 

    def test_remove_tempfile(self):
        shutil.rmtree('ASOS_data')
        if not os.path.exists('ASOS_data'):
            assertion = True
        self.assertTrue(assertion == True, 'All testing files were not removed')

    def tearDownClass(self): 
       ASOS.driver.quit()
    

if __name__ == '__main__':
    unittest.main()   
    
    
# %%
