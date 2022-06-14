#%%
# Unit Testing for load_more_button()
import selenium
import unittest
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS

class TestFunction_3(unittest.TestCase):
    @classmethod 
    def setUpClass(self):
      new_scraper = ASOS
      ASOS._load_more_products()
        
# Unit Test 1: Test whether the load_button works
    def test_load_more_button(self):
      self.assertTrue(ASOS.unit_Test_Load_1 == 'True', "The load more button was not clicked")
    
    def test_load_multiple(self):
      self.assertTrue(ASOS.unit_loaded_pages == True , "The load_more_products function did not finish")
 
    def test_loaded_pages(self):
      actual_value2 = ASOS.load_pages
      expected_value2 = ASOS.n_pages
      self.assertEqual(expected_value2, actual_value2, f"{ASOS.load_pages} pages are not equal to {ASOS.n_pages} pages.")
        
    @classmethod
    def tearDownClass(self):
      print('\n Testing load page complete')
    
if __name__ == '__main__':
    unittest.main()
    
# %%
