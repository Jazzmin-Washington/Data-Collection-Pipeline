#%%
# Unit Testing for load_more_button()
import selenium
from selenium.webdriver import Chrome
import unittest
import time
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS

class TestFunction_2(unittest.TestCase):
    def setUpClass():
        new_scraper = ASOS
        ASOS._nav_to_sale_pg()
       
# Unit Test 1: Test whether the load_button works
    def test_webpage_site(self):
        actual = ASOS.driver.current_url
        expected = 'https://www.asos.com/women/sale/cat/?cid=7046&nlid=ww|sale|shop+by+product|sale+view+all'
        self.assertEqual(actual, expected, 'Driver did not go to the sale webpage')


    def tearDownClass():
        print('\n Navigation complete')
    

if __name__ == '__main__':
    unittest.main()
    
