#%% 
# Unit Test for Saving Images
import selenium
from selenium.webdriver import Chrome
import os
import unittest
import shutil
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS

class TestFunction_7(unittest.TestCase):
    def setUpClass():
        new_scraper = ASOS
        ASOS._get_images()
  
    def test_image_sources(self):
        for image in range(len(ASOS.imagesrc_list)):
            self.assertTrue(ASOS.imagesrc_list[image] == ASOS.full_item_list['image'][image], 'Image srcs do not match from website scrape')
    
    def test_check_images(self):
        for i in ASOS.test_images:
            self.assertTrue(ASOS.test_images[i] == True, 'Each image was not downloaded successfully')

    def tearDownClass():
        ASOS.driver.quit()

if __name__ == '__main__':
    unittest.main()
        
        
