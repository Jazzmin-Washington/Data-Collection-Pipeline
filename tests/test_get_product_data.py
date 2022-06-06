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


class TestGetProductData(unittest.TestCase):

    def setUpClass():
        ASOS.load_and_accept_cookies()
        time.sleep(1)
        ASOS.nav_to_sale_pg()
        ASOS.get_product_links()
        ASOS.get_product_data()
    
    def test_link_url(self):
        for i in range(10):
            ASOS.driver.implicitly_wait(10)
            ASOS.driver.get(ASOS.shop_link_list[i])
            ASOS.actions.move_to_element(ASOS.show_more_button).click()
           

            expected = ASOS.shop_link_list[i]
            actual = ASOS.driver.current_url
            self.assertEqual(expected, actual)

            try:
                ASOS.driver.implicitly_wait(10)
                actual_2 =ASOS.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[1]/div/div[2]/div[2]/div[1]/h1').text
                expected_2 = ASOS.full_item_list['product_name'][i]
                self.assertEqual(expected_2, actual_2)
            except NoSuchElementException or AssertionError:
                print(f'Product Name did not match for link number {[i]}')
            
            
            try: 
                ASOS.driver.implicitly_wait(10)
                actual_3 = ASOS.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/span[2]/span[4]/span[1]').text.replace("Now", '')
                expected_3 = ASOS.full_item_list['sale_price'][i]
                self.assertEqual(expected_3, actual_3)
            except NoSuchElementException or AssertionError:
                print(f'Sale Price did not match for link number {[i]}')
                

            try: 
                ASOS.driver.implicitly_wait(10)
                actual_4 = ASOS.driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/section[2]/div/div/div/div[1]/div').text.replace("PRODUCT DETAILS\n", "")
                expected_4 = ASOS.full_item_list['product_details'][i]
                self.assertIn(actual_4, expected_4)
            except NoSuchElementException or AssertionError:
                print(f'Description did not match for link number {[i]}')
            

    def tearDownClass(): 
       ASOS.driver.quit()
    

if __name__ == '__main__':
    unittest.main()   
    def tearDownClass(self): 
       ASOS.driver.quit()
    

if __name__ == '__main__':
    unittest.main()   
    
    
# %%

    
    
# %%
