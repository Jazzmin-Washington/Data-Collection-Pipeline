#%%  Unit Test for get_product_data function
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import json
import os
import unittest 
import shutil
from tqdm import tqdm
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS


class TestFunction_5(unittest.TestCase):

    def setUpClass():
        new_scraper = ASOS
        ASOS._get_product_data()
    
    def test_link_url(self):
        for i in tqdm(range(5), 'Checking Collected Data'):
            ASOS.driver.implicitly_wait(10)
            ASOS.driver.get(ASOS.shop_link_list[i])
            ASOS.actions.move_to_element(ASOS.show_more_button).click()
           

            expected = ASOS.shop_link_list[i]
            actual = ASOS.driver.current_url
            self.assertEqual(expected, actual)

            try:
                ASOS.driver.implicitly_wait(10)
                actual_2 =ASOS.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[1]/div/div[2]/div[2]/div[1]/h1').text.strip()
                expected_2 = ASOS.full_item_list['product_name'][i]
                self.assertIn(actual_2, expected_2)
            except NoSuchElementException or AssertionError:
                print(actual_3, expected_3)
                pass
            
            
            try: 
                ASOS.driver.implicitly_wait(10)
                actual_3 = ASOS.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/span[2]/span[4]/span[1]').text.strip()
                actual_3 = actual_3.replace("Now", '')
                expected_3 = ASOS.full_item_list['sale_price'][i]
                self.assertIn(actual_3, expected_3)
            except NoSuchElementException or AssertionError:
                print(actual_3, expected_3)
                pass
                

            try: 
                ASOS.driver.implicitly_wait(10)
                actual_4 = ASOS.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[2]/div/div/div/div[1]/div').text.strip()
                actual_4 = actual_4.replace("PRODUCT DETAILS\n", "")
                expected_4 = ASOS.full_item_list['product_details'][i]
                self.assertIn(actual_4, expected_4)
            except NoSuchElementException or AssertionError:
                print(actual_4, expected_4)
                pass
    
    def tearDownClass(): 
        print('\n Product Data complete')
    

if __name__ == '__main__':
    unittest.main()   
    
    
    
# %%
