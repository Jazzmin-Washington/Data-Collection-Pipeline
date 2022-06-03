#%% 
# Unit Test for Saving Images
import selenium
from selenium.webdriver import Chrome
import os
import unittest
import shutil
from unittest import TestCase
from scrapers.Data_Collection_ASOS_small_batch_for_testing import ASOS

class TestSaveImages(unittest.TestCase):
    def setUpClass(self):
        ASOS.get_images()
  
    def test_image_sources(self):
        for image in range(len(ASOS.imagesrc_list)):
            self.assertTrue(ASOS.imagesrc_list[image] == ASOS.full_item_list['image'][image], 'Image srcs do not match from website scrape')
    
    def test_check_images(self):
        for image in ASOS.test_images:
            self.assertTrue(image == True, 'Each image was not downloaded successfully')

    def test_remove_tempfile(self):
        if os.path.exists('ASOS_data/image'):
            shutil.rmtree('ASOS_data/image')
            assertion = True
        self.assertTrue(assertion == True)

    
    def tearDownClass(self):
        ASOS.driver.quit()

if __name__ == '__main__':
    unittest.main()
        