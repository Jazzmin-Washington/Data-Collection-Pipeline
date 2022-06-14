#%%  Unit Test for get_link function
from os import link
import selenium
import unittest
import time
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS

class TestFunction_4(unittest.TestCase):
    def setUpClass():
        new_scraper = ASOS
        ASOS._get_product_links()

    def test_number_of_links(self):
        actual_value = len(ASOS.shop_link_list)
        expected_value = 432
        self.assertEqual(expected_value, actual_value, 'There has been an error gathering test links')
    
    def test_link_url(self):
        for i in range(5):
            ASOS.driver.implicitly_wait(10)
            ASOS.driver.get(ASOS.shop_link_list[i])
            key = ASOS.driver.current_url
            container = ASOS.shop_link_list
            self.assertIn(key, container, 'There has been an error gathering the product links') 

    def tearDownClass():
       print('\n Link Collection Complete')

if __name__ == '__main__':
    unittest.main()
    

    
