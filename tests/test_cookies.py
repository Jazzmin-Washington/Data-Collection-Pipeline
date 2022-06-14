#%%
# Unit Testing for load_and_accept_cookies_button
import selenium
from selenium.webdriver import Chrome
import unittest
import time
from unittest import TestCase
import time
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS



class TestFunction_1(unittest.TestCase):
    @classmethod
    def setUpClass(self):
      new_scraper = ASOS
      ASOS._load_and_accept_cookies()
   
# Unit Test 1: Test whether the load_and_accept_cookies_button_works
    def test_cookies(self):
      self.assertTrue(ASOS.unit_Test_Cookies == 'True', "The cookies button was not clicked")
  
    @classmethod
    def tearDownClass(self):
      print('\n Cookies have been accepted')

if __name__ == '__main__':
    unittest.main()
