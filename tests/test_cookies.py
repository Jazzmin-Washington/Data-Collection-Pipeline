#%%
# Unit Testing for load_and_accept_cookies_button
import selenium
from selenium.webdriver import Chrome
import unittest
from unittest import TestCase


class TestLoadAndAcceptCookies(unittest.TestCase):
    @classmethod
    def setUpClass(self):
      ASOS.driver.implicitly_wait(5)
      ASOS.load_and_accept_cookies()
   
# Unit Test 1: Test whether the load_and_accept_cookies_button_works
    def test_cookies(self):
      self.assertTrue(ASOS.unit_Test_Cookies == 'True', "The cookies button was not clicked")
  
    @classmethod
    def tearDownClass(self):
      ASOS.driver.quit()
      
    
# %%
